# LazyOwn API Reference

> Generated offline by readmenator: 735 modules, 14072 documented entities, documentation coverage 72.7% (6453/8878 public items). Deterministic, zero tokens: signatures from source, docs parsed from Google, NumPy, reST, Javadoc/JSDoc/Doxygen, C# XML, and Rustdoc comments.

Navigate: [Interactive architecture and flows](flows.html) | [Architecture and flows (Mermaid)](architecture.md) | [Class hierarchy](classes.md) | [General index](genindex.md) | [Coverage and warnings](COVERAGE.md) | [`api/index.json`](api/index.json) | [HTML browser](index.html)

Languages: asm (1), c (15), cpp (1), cs (1), h (1), js (6), lua (26), php (1), py (625), sh (58)

## Modules

### `.`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`DEPLOY.sh`](modules/DEPLOY.sh.md) |  | 0 | 3 | 50.0% |
| [`__init__`](modules/init__.py.md) |  | 0 | 0 | 0.0% |
| [`banner`](modules/banner.py.md) | banner.py | 0 | 3 | 25.0% |
| [`bootstrap.sh`](modules/bootstrap.sh.md) | LazyOwn bootstrap installer (one-liner entry point). | 0 | 16 | 5.9% |
| [`discord_c2`](modules/discord_c2.py.md) |  | 2 | 18 | 0.0% |
| [`fast_run_as_r00t.sh`](modules/fast_run_as_r00t.sh.md) | fast_run_as_r00t.sh — LazyOwn full-stack orchestrator Speed-run launcher: brings up every core service in a tmux session. | 0 | 12 | 84.6% |
| [`gen_cert.sh`](modules/gen_cert.sh.md) | Verifica si se pasó una IP | 0 | 0 | 100.0% |
| [`install.sh`](modules/install.sh.md) | LazyOwn installer. | 0 | 16 | 5.9% |
| [`key`](modules/key.py.md) |  | 0 | 1 | 0.0% |
| [`lazy_sentinel4`](modules/lazy_sentinel4.py.md) |  | 6 | 41 | 8.3% |
| [`lazyc2`](modules/lazyc2.py.md) |  | 3 | 225 | 38.4% |
| [`lazyown`](modules/lazyown.py.md) | lazyown | 1 | 74 | 97.4% |
| [`mutate.sh`](modules/mutate.sh.md) |  | 0 | 0 | 0.0% |
| [`pwntomate`](modules/pwntomate.py.md) | This software must not be used by military or secret service organisations. | 0 | 0 | 100.0% |
| [`py2elf.sh`](modules/py2elf.sh.md) | Nombre del script: py2elf.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Descripción: Este script... | 0 | 0 | 100.0% |
| [`readmeneitor`](modules/readmeneitor.py.md) | readmeneitor.py — Automated documentation generator for LazyOwn RedTeam Framework. | 0 | 11 | 100.0% |
| [`run_telegram_hermes.sh`](modules/run_telegram_hermes.sh.md) | Launcher for telegram_hermes.py Uses the dedicated venv with python-telegram-bot dependencies | 0 | 0 | 100.0% |
| [`run_topoexploit_agent.sh`](modules/run_topoexploit_agent.sh.md) | Run TopoExploit against an ExploitGym task using the local model. | 0 | 2 | 33.3% |
| [`setup`](modules/setup.py.md) | Compatibility shim for legacy ``python setup.py`` invocations. | 0 | 0 | 100.0% |
| [`slack_c2_bot`](modules/slack_c2_bot.py.md) | slack_c2_bot_socket.py | 1 | 15 | 5.9% |
| [`telegram_c2`](modules/telegram_c2.py.md) |  | 2 | 15 | 5.6% |
| [`telegram_hermes`](modules/telegram_hermes.py.md) | telegram_hermes.py LazyOwn Telegram Bot with Hermes Gateway Integration | 1 | 28 | 10.0% |
| [`testmeneitor`](modules/testmeneitor.py.md) |  | 0 | 4 | 0.0% |
| [`user_split.sh`](modules/user_split.sh.md) |  | 0 | 0 | 0.0% |
| [`utils`](modules/utils.py.md) | utils.py | 4 | 110 | 85.2% |

### `.claude/skills/run-lazyown`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`.claude/skills/run-lazyown/driver.sh`](modules/claude.skills.run-lazyown.driver.sh.md) | Build and drive LazyOwn inside its Docker sandbox (Debian container). | 0 | 0 | 100.0% |

### `cli`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`cli`](modules/cli.__init__.py.md) | LazyOwn CLI infrastructure. | 0 | 0 | 100.0% |
| [`cli.aliases`](modules/cli.aliases.py.md) | Declarative cmd2 alias loader. | 0 | 3 | 100.0% |
| [`cli.assign`](modules/cli.assign.py.md) | ``assign`` business logic. | 0 | 1 | 100.0% |
| [`cli.auto_crypto`](modules/cli.auto_crypto.py.md) | Automatic encryption of sensitive session data on app open/close. | 2 | 7 | 100.0% |
| [`cli.autosuggest`](modules/cli.autosuggest.py.md) | Ghost-text autosuggest engine for the LazyOwn cmd2 shell. | 7 | 18 | 96.2% |
| [`cli.banner_config`](modules/cli.banner_config.py.md) | Configurable Neon Box banner for the LazyOwn interactive shell. | 25 | 56 | 23.2% |
| [`cli.chain_mode`](modules/cli.chain_mode.py.md) | Interactive kill-chain chaining coordinator. | 5 | 9 | 100.0% |
| [`cli.cli_enhancements`](modules/cli.cli_enhancements.py.md) | CLI enhancement primitives for the LazyOwn interactive shell. | 21 | 31 | 54.7% |
| [`cli.command_chain`](modules/cli.command_chain.py.md) | Command chain registry: explicit prerequisites and dynamic next steps. | 7 | 15 | 100.0% |
| [`cli.command_explorer`](modules/cli.command_explorer.py.md) | Interactive command explorer by phase and goal for the LazyOwn shell. | 2 | 4 | 100.0% |
| [`cli.command_form`](modules/cli.command_form.py.md) | Textual form-mode launcher for LazyOwn commands. | 4 | 10 | 100.0% |
| [`cli.config_history`](modules/cli.config_history.py.md) | In-memory configuration history with undo and diff. | 2 | 7 | 100.0% |
| [`cli.config_status`](modules/cli.config_status.py.md) | Simplified configuration status display for the LazyOwn shell. | 2 | 3 | 100.0% |
| [`cli.confirm`](modules/cli.confirm.py.md) | Shared interactive confirmation helpers with safe non-TTY behaviour. | 0 | 1 | 100.0% |
| [`cli.contextual_help`](modules/cli.contextual_help.py.md) | Contextual help system for the LazyOwn shell. | 3 | 5 | 100.0% |
| [`cli.dashboard_layout`](modules/cli.dashboard_layout.py.md) | Responsive layout decisions for the Textual operator dashboard. | 1 | 2 | 100.0% |
| [`cli.dashboard_tui`](modules/cli.dashboard_tui.py.md) | LazyOwn operator dashboard — a full-screen Textual TUI. | 1 | 13 | 73.3% |
| [`cli.doctor`](modules/cli.doctor.py.md) | Environment health check (preflight doctor) for the LazyOwn framework. | 3 | 16 | 95.0% |
| [`cli.engagement_hooks`](modules/cli.engagement_hooks.py.md) | Curiosity-driven engagement engine for LazyOwn. | 1 | 5 | 100.0% |
| [`cli.exploit_advisor`](modules/cli.exploit_advisor.py.md) | Exploit advisor: connects nmap scan results to exploit search and next-step commands. | 3 | 8 | 91.7% |
| [`cli.exploration`](modules/cli.exploration.py.md) | Exploration engine: trigger and OS aware addon/tool matching. | 11 | 29 | 100.0% |
| [`cli.exploration_view`](modules/cli.exploration_view.py.md) | Rich-based renderers for the exploration engine. | 0 | 1 | 100.0% |
| [`cli.fuzzy_match`](modules/cli.fuzzy_match.py.md) | Non-interactive fuzzy matching reusing the picker's scorer. | 1 | 2 | 100.0% |
| [`cli.fuzzy_picker`](modules/cli.fuzzy_picker.py.md) | Curses-based fuzzy dropdown picker for the LazyOwn interactive shell. | 8 | 13 | 68.2% |
| [`cli.graph_advisor`](modules/cli.graph_advisor.py.md) | Graph-aware advisor backed by the graphify knowledge graph. | 8 | 32 | 39.0% |
| [`cli.graph_overlay`](modules/cli.graph_overlay.py.md) | Textual overlay over :mod:`cli.graph_advisor`. | 4 | 6 | 100.0% |
| [`cli.headless`](modules/cli.headless.py.md) | Headless / non-interactive runner for automated pipelines. | 1 | 5 | 85.7% |
| [`cli.killchain`](modules/cli.killchain.py.md) | Self-populating kill-chain progress derived from the daemon event stream. | 1 | 1 | 100.0% |
| [`cli.lazy_monitor`](modules/cli.lazy_monitor.py.md) | Live worker-visibility monitor for the autonomous loop. | 1 | 17 | 100.0% |
| [`cli.lazy_orchestrator`](modules/cli.lazy_orchestrator.py.md) | Orchestrator admin console for the autonomous loop. | 2 | 25 | 100.0% |
| [`cli.lazynmap_post`](modules/cli.lazynmap_post.py.md) | Post-scan side effects executed at the tail of ``do_lazynmap``. | 2 | 1 | 100.0% |
| [`cli.marketplace_config`](modules/cli.marketplace_config.py.md) | Interactive marketplace manager for LazyOwn lazyaddons, plugins, and tools. | 5 | 18 | 45.8% |
| [`cli.noise_verbs`](modules/cli.noise_verbs.py.md) | Canonical non-actionable verb registry for post-command surfaces. | 0 | 0 | 100.0% |
| [`cli.ops_commands`](modules/cli.ops_commands.py.md) | Power-user operator commands: ctx, tgrep, phase, note, l00t, pivot, tasks, sitrep, scans. | 1 | 24 | 100.0% |
| [`cli.output_mode`](modules/cli.output_mode.py.md) | Structured output modes and dry-run rendering for CLI commands. | 2 | 4 | 100.0% |
| [`cli.palette`](modules/cli.palette.py.md) | Read-only loader for ``cli/command_index.json``. | 1 | 10 | 100.0% |
| [`cli.palette_command`](modules/cli.palette_command.py.md) | Pure logic for the operator-facing ``palette`` command. | 11 | 29 | 87.8% |
| [`cli.palette_graph`](modules/cli.palette_graph.py.md) | Graph-aware neighbour lookups for the operator command palette. | 3 | 6 | 100.0% |
| [`cli.palette_overlay`](modules/cli.palette_overlay.py.md) | Textual Cmd-K palette overlay for the LazyOwn shell. | 3 | 4 | 100.0% |
| [`cli.palette_telemetry`](modules/cli.palette_telemetry.py.md) | Behavioural telemetry derived from ``sessions/LazyOwn_session_report.csv``. | 4 | 7 | 100.0% |
| [`cli.phase_labels`](modules/cli.phase_labels.py.md) | Canonical human-readable labels for kill-chain command phases. | 0 | 1 | 100.0% |
| [`cli.plugin_tiers`](modules/cli.plugin_tiers.py.md) | Plugin tiers and operator ratings for the marketplace. | 0 | 7 | 100.0% |
| [`cli.protips`](modules/cli.protips.py.md) | Pro tips system for the LazyOwn shell. | 1 | 3 | 100.0% |
| [`cli.purple_tui`](modules/cli.purple_tui.py.md) | Purple Team Dashboard — Textual TUI for engagement monitoring. | 1 | 5 | 42.9% |
| [`cli.reactive_hints`](modules/cli.reactive_hints.py.md) | Non-blocking inline hint renderer for the LazyOwn cmd2 shell. | 1 | 7 | 100.0% |
| [`cli.reasoning_stream`](modules/cli.reasoning_stream.py.md) | Operator-facing view over the autonomous daemon decision log. | 1 | 4 | 100.0% |
| [`cli.recommendation`](modules/cli.recommendation.py.md) | Unified next-best-action engine: the single source of truth for "what next". | 7 | 5 | 100.0% |
| [`cli.recommendation_signals`](modules/cli.recommendation_signals.py.md) | Concrete :class:`cli.recommendation.RecommendationSignal` adapters. | 7 | 18 | 92.3% |
| [`cli.recon_plan`](modules/cli.recon_plan.py.md) | Reconnaissance plan generator built on top of :mod:`cli.exploration`. | 3 | 5 | 100.0% |
| [`cli.registry`](modules/cli.registry.py.md) | ``cmd2.CommandSet`` discovery and registration for ``cli.commands``. | 0 | 2 | 100.0% |
| [`cli.scope_guard`](modules/cli.scope_guard.py.md) | Authorization scope guard for offensive command execution. | 3 | 6 | 100.0% |
| [`cli.session_hud`](modules/cli.session_hud.py.md) | Compact session HUD: the numbers no other command shows. | 2 | 6 | 100.0% |
| [`cli.session_resumer`](modules/cli.session_resumer.py.md) | Session resumer for the LazyOwn shell. | 3 | 2 | 100.0% |
| [`cli.sessions_browser`](modules/cli.sessions_browser.py.md) | Textual browser for the LazyOwn ``sessions/`` directory. | 6 | 9 | 100.0% |
| [`cli.show`](modules/cli.show.py.md) | Pretty-print the live payload for the operator. | 0 | 1 | 100.0% |
| [`cli.splash`](modules/cli.splash.py.md) | Animated splash overlay for the LazyOwn first-run experience. | 4 | 4 | 66.7% |
| [`cli.status_bar`](modules/cli.status_bar.py.md) | Persistent operator status bar for the LazyOwn cmd2 shell. | 12 | 30 | 100.0% |
| [`cli.style`](modules/cli.style.py.md) | Centralised TUI style tokens for the LazyOwn operator surface. | 0 | 4 | 100.0% |
| [`cli.surface_graph`](modules/cli.surface_graph.py.md) | Network surface graph reader for the LazyOwn shell. | 5 | 10 | 93.8% |
| [`cli.surface_tui`](modules/cli.surface_tui.py.md) | Terminal renderer for the LazyOwn network surface graph. | 1 | 3 | 100.0% |
| [`cli.themes`](modules/cli.themes.py.md) | Theme registry for the LazyOwn TUI surfaces. | 1 | 2 | 100.0% |
| [`cli.timeline_browser`](modules/cli.timeline_browser.py.md) | Textual scrubber over ``sessions/LazyOwn_session_report.csv``. | 5 | 8 | 100.0% |
| [`cli.tips_engine`](modules/cli.tips_engine.py.md) | Unified post-command tips engine: single coordination point for all suggestion surfaces. | 2 | 9 | 100.0% |
| [`cli.toast_bus`](modules/cli.toast_bus.py.md) | Non-blocking toast notification subsystem for the LazyOwn shell. | 6 | 30 | 100.0% |
| [`cli.tui_theme`](modules/cli.tui_theme.py.md) | Operator-facing ``tui_theme`` command logic. | 0 | 1 | 100.0% |
| [`cli.tutorial`](modules/cli.tutorial.py.md) | Interactive post-install tutorial for the LazyOwn framework. | 1 | 6 | 100.0% |
| [`cli.wizard`](modules/cli.wizard.py.md) | Guided first-run setup wizard for the LazyOwn framework. | 3 | 3 | 100.0% |
| [`cli.wizard_scope`](modules/cli.wizard_scope.py.md) | Partial wizard scope: show current state or edit selected fields only. | 2 | 2 | 100.0% |

### `cli/commands`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`cli.commands`](modules/cli.commands.__init__.py.md) | Phase-scoped CommandSet modules. | 0 | 0 | 100.0% |
| [`cli.commands._base`](modules/cli.commands._base.py.md) | Base class for phase-scoped ``CommandSet`` modules. | 1 | 5 | 100.0% |
| [`cli.commands._dormancy`](modules/cli.commands._dormancy.py.md) | Dormancy marker for incrementally migrated command sets. | 1 | 1 | 100.0% |
| [`cli.commands.active_directory`](modules/cli.commands.active_directory.py.md) | Active Directory attack commands — Kerberos, tickets, delegation, DACL, GPO, kerberoasting. | 1 | 7 | 100.0% |
| [`cli.commands.ai`](modules/cli.commands.ai.py.md) | Artificial Intelligence command set. | 1 | 6 | 100.0% |
| [`cli.commands.anti_forensics`](modules/cli.commands.anti_forensics.py.md) | Anti-Forensics command set. | 1 | 6 | 100.0% |
| [`cli.commands.applocker_bypass`](modules/cli.commands.applocker_bypass.py.md) | AppLocker and WDAC bypass command set. | 1 | 7 | 100.0% |
| [`cli.commands.audit`](modules/cli.commands.audit.py.md) | Audit-mode CommandSet: fuzzy finder, forms, status tail, transcript grep. | 1 | 7 | 88.9% |
| [`cli.commands.automation`](modules/cli.commands.automation.py.md) | Automation command set — credential reuse, conditional hooks, operator profiles. | 1 | 12 | 100.0% |
| [`cli.commands.bitm`](modules/cli.commands.bitm.py.md) | Browser-in-the-Middle CLI command set. | 1 | 1 | 100.0% |
| [`cli.commands.bof_registry`](modules/cli.commands.bof_registry.py.md) | BOF marketplace CommandSet — Beacon Object File discovery, install, and execution. | 1 | 7 | 100.0% |
| [`cli.commands.c2_profile`](modules/cli.commands.c2_profile.py.md) | C2 profile CommandSet — extended malleable C2 profiles (TLS, DNS, SMB, WS). | 1 | 4 | 100.0% |
| [`cli.commands.caldera`](modules/cli.commands.caldera.py.md) | Caldera-style command set — operation lifecycle, TTP coverage, and planner. | 1 | 16 | 100.0% |
| [`cli.commands.campaign`](modules/cli.commands.campaign.py.md) | Campaign export/import commands — portable engagement packages. | 1 | 1 | 100.0% |
| [`cli.commands.catalog`](modules/cli.commands.catalog.py.md) | Command catalog — browse all registered commands by keyword, phase or category. | 1 | 2 | 100.0% |
| [`cli.commands.cicd`](modules/cli.commands.cicd.py.md) | CI/CD Enumeration command set. | 1 | 5 | 100.0% |
| [`cli.commands.cli_auth`](modules/cli.commands.cli_auth.py.md) | CLI authentication command set — login/logout/whoami. | 1 | 4 | 100.0% |
| [`cli.commands.cloud`](modules/cli.commands.cloud.py.md) | Cloud attack command set. | 1 | 5 | 100.0% |
| [`cli.commands.cloud_attacks`](modules/cli.commands.cloud_attacks.py.md) | Cloud attack commands — Azure AD/Entra ID, AWS, GCP, Kubernetes, cross-cloud, SaaS. | 1 | 6 | 100.0% |
| [`cli.commands.collaboration`](modules/cli.commands.collaboration.py.md) | Collaboration CLI commands — multi-operator teamwork from the shell. | 1 | 5 | 100.0% |
| [`cli.commands.command_and_control`](modules/cli.commands.command_and_control.py.md) | Command & Control command set. | 1 | 6 | 100.0% |
| [`cli.commands.command_and_control_migrated`](modules/cli.commands.command_and_control_migrated.py.md) | command_and_control commands migrated from lazyown.py. | 1 | 22 | 95.8% |
| [`cli.commands.containers`](modules/cli.commands.containers.py.md) | Container and Kubernetes attack command set. | 1 | 6 | 100.0% |
| [`cli.commands.cred`](modules/cli.commands.cred.py.md) | Credential Access command set (pending). | 1 | 9 | 100.0% |
| [`cli.commands.cred_migrated`](modules/cli.commands.cred_migrated.py.md) | cred commands migrated from lazyown.py. | 1 | 22 | 95.8% |
| [`cli.commands.crystal_ball`](modules/cli.commands.crystal_ball.py.md) | Crystal Ball CLI command set — privilege escalation vector prediction. | 1 | 2 | 100.0% |
| [`cli.commands.daemon_ctl`](modules/cli.commands.daemon_ctl.py.md) | Autonomous daemon control extracted from the miscellaneous cluster. | 1 | 7 | 100.0% |
| [`cli.commands.database`](modules/cli.commands.database.py.md) | Database commands — workspace isolation, host/service/vuln management, nmap import, export, and status reporting. | 1 | 13 | 100.0% |
| [`cli.commands.defaults`](modules/cli.commands.defaults.py.md) | Build-defaults inspection and override command set. | 1 | 1 | 100.0% |
| [`cli.commands.demo`](modules/cli.commands.demo.py.md) | End-to-end demo command — MCP registration plus the golden path. | 1 | 1 | 100.0% |
| [`cli.commands.diagnostics`](modules/cli.commands.diagnostics.py.md) | Diagnostics CommandSet (Tier 2 pilot). | 1 | 2 | 100.0% |
| [`cli.commands.dns_exfil`](modules/cli.commands.dns_exfil.py.md) | DNS exfiltration and covert channel command set. | 1 | 6 | 100.0% |
| [`cli.commands.dpapi`](modules/cli.commands.dpapi.py.md) | DPAPI credential harvesting command set. | 1 | 3 | 100.0% |
| [`cli.commands.edr_detect`](modules/cli.commands.edr_detect.py.md) | EDR Detection command set. | 1 | 3 | 100.0% |
| [`cli.commands.encoding`](modules/cli.commands.encoding.py.md) | Encoding commands extracted from misc_migrated.py. | 1 | 12 | 100.0% |
| [`cli.commands.enum`](modules/cli.commands.enum.py.md) | Enumeration command set. | 1 | 10 | 100.0% |
| [`cli.commands.estorides`](modules/cli.commands.estorides.py.md) | Estorides integration commands — bidirectional feedback loop with passive OSINT. | 1 | 4 | 100.0% |
| [`cli.commands.evasive_payload`](modules/cli.commands.evasive_payload.py.md) | Auto-Adaptive Payload command set. | 1 | 5 | 100.0% |
| [`cli.commands.exfiltration`](modules/cli.commands.exfiltration.py.md) | Data Exfiltration command set. | 1 | 27 | 100.0% |
| [`cli.commands.exploit`](modules/cli.commands.exploit.py.md) | Exploitation command set (pending activation). | 1 | 10 | 100.0% |
| [`cli.commands.exploit_migrated`](modules/cli.commands.exploit_migrated.py.md) | exploit commands migrated from lazyown.py. | 1 | 49 | 98.0% |
| [`cli.commands.exploitgym`](modules/cli.commands.exploitgym.py.md) | ExploitGym CLI command set — real-world exploit benchmark harness. | 1 | 1 | 100.0% |
| [`cli.commands.help_ui`](modules/cli.commands.help_ui.py.md) | Help, tutorial and phase guidance extracted from the miscellaneous cluster. | 1 | 14 | 100.0% |
| [`cli.commands.infra`](modules/cli.commands.infra.py.md) | Disposable infrastructure commands -- redirectors, C2, cloud IaC. | 1 | 1 | 100.0% |
| [`cli.commands.lab`](modules/cli.commands.lab.py.md) | Lab environment commands -- spin up vulnerable practice targets. | 1 | 1 | 100.0% |
| [`cli.commands.lateral`](modules/cli.commands.lateral.py.md) | Lateral Movement command set (pending). | 1 | 8 | 100.0% |
| [`cli.commands.lateral_migrated`](modules/cli.commands.lateral_migrated.py.md) | lateral commands migrated from lazyown.py. | 1 | 21 | 95.7% |
| [`cli.commands.lazyloop`](modules/cli.commands.lazyloop.py.md) | Lazy queue and misc command set. | 1 | 10 | 100.0% |
| [`cli.commands.lazyops`](modules/cli.commands.lazyops.py.md) | Lazy autonomous loop commands (single orchestrator, lazy_* surface). | 1 | 57 | 96.6% |
| [`cli.commands.marketplace`](modules/cli.commands.marketplace.py.md) | Plugin/addon marketplace commands. | 1 | 2 | 100.0% |
| [`cli.commands.mcp_bridge`](modules/cli.commands.mcp_bridge.py.md) | MCP verb bridge — one command language for operators and agents. | 1 | 10 | 100.0% |
| [`cli.commands.misc_migrated`](modules/cli.commands.misc_migrated.py.md) | misc commands migrated from lazyown.py. | 1 | 29 | 96.8% |
| [`cli.commands.mobile_macos`](modules/cli.commands.mobile_macos.py.md) | Mobile & macOS exploitation command set. | 1 | 5 | 100.0% |
| [`cli.commands.module_manager`](modules/cli.commands.module_manager.py.md) | Module management commands — search, use, back, and active module context. | 1 | 3 | 100.0% |
| [`cli.commands.nethelpers`](modules/cli.commands.nethelpers.py.md) | Network helpers extracted from the miscellaneous cluster. | 1 | 10 | 100.0% |
| [`cli.commands.opsec_cleanup`](modules/cli.commands.opsec_cleanup.py.md) | OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory, network. | 1 | 8 | 100.0% |
| [`cli.commands.orchestration`](modules/cli.commands.orchestration.py.md) | Orchestration CommandSet: operator-facing surface for the new modules. | 2 | 2 | 100.0% |
| [`cli.commands.payload_arsenal`](modules/cli.commands.payload_arsenal.py.md) | Payload arsenal commands — dotnet, reflective DLL, staged delivery, polymorphic, macOS/Linux payloads. | 1 | 6 | 100.0% |
| [`cli.commands.payload_generation`](modules/cli.commands.payload_generation.py.md) | Payload generation commands — list payloads and generate. | 1 | 1 | 100.0% |
| [`cli.commands.persist`](modules/cli.commands.persist.py.md) | Persistence command set (pending). | 1 | 9 | 100.0% |
| [`cli.commands.persist_migrated`](modules/cli.commands.persist_migrated.py.md) | persist commands migrated from lazyown.py. | 1 | 24 | 96.2% |
| [`cli.commands.phishing_wizard`](modules/cli.commands.phishing_wizard.py.md) | Phishing Wizard command set. | 1 | 3 | 100.0% |
| [`cli.commands.pivoting`](modules/cli.commands.pivoting.py.md) | Intelligent Pivoting command set. | 1 | 5 | 100.0% |
| [`cli.commands.postexp`](modules/cli.commands.postexp.py.md) | Post-Exploitation command set (pending). | 1 | 8 | 100.0% |
| [`cli.commands.postexp_migrated`](modules/cli.commands.postexp_migrated.py.md) | postexp commands migrated from lazyown.py. | 1 | 37 | 97.4% |
| [`cli.commands.privilege_escalation`](modules/cli.commands.privilege_escalation.py.md) | Privilege Escalation command set. | 1 | 14 | 100.0% |
| [`cli.commands.purple_team`](modules/cli.commands.purple_team.py.md) | Purple Team CommandSet: closed-loop offensive detection measurement. | 1 | 8 | 100.0% |
| [`cli.commands.pwn`](modules/cli.commands.pwn.py.md) | Autonomous exploitation and LOLBAS command set. | 1 | 7 | 100.0% |
| [`cli.commands.recon`](modules/cli.commands.recon.py.md) | Reconnaissance command set. | 1 | 12 | 100.0% |
| [`cli.commands.recon_migrated`](modules/cli.commands.recon_migrated.py.md) | recon commands migrated from lazyown.py. | 1 | 28 | 96.7% |
| [`cli.commands.redteam_gym`](modules/cli.commands.redteam_gym.py.md) | Red Team Gym CLI command set — gamified pentest training. | 1 | 1 | 100.0% |
| [`cli.commands.resource_scripting`](modules/cli.commands.resource_scripting.py.md) | Resource script commands — run .ls scripts, record macros, spool output. | 1 | 4 | 100.0% |
| [`cli.commands.scan`](modules/cli.commands.scan.py.md) | Scanning command set. | 1 | 16 | 100.0% |
| [`cli.commands.scan_migrated`](modules/cli.commands.scan_migrated.py.md) | scan commands migrated from lazyown.py. | 1 | 45 | 97.9% |
| [`cli.commands.security`](modules/cli.commands.security.py.md) | OPSEC and security commands — risk scoring, credential sealing, rotation. | 1 | 7 | 77.8% |
| [`cli.commands.session_ops`](modules/cli.commands.session_ops.py.md) | Session and campaign operations extracted from the miscellaneous cluster. | 1 | 33 | 100.0% |
| [`cli.commands.shellsys`](modules/cli.commands.shellsys.py.md) | Local shell and system extracted from the miscellaneous cluster. | 1 | 10 | 100.0% |
| [`cli.commands.sleep_obfuscation`](modules/cli.commands.sleep_obfuscation.py.md) | Sleep obfuscation CommandSet — beacon memory evasion technique management. | 1 | 3 | 100.0% |
| [`cli.commands.socks_proxy`](modules/cli.commands.socks_proxy.py.md) | SOCKS proxy CommandSet — beacon tunneling configuration. | 1 | 3 | 100.0% |
| [`cli.commands.supply_chain`](modules/cli.commands.supply_chain.py.md) | Supply Chain Attack command set. | 1 | 3 | 100.0% |
| [`cli.commands.surface`](modules/cli.commands.surface.py.md) | Attack-surface operations: confirmed discovery scans, estorides fusion. | 1 | 2 | 100.0% |
| [`cli.commands.ux`](modules/cli.commands.ux.py.md) | Usability commands: hud, undo, config_diff, cheat, suggest. | 1 | 6 | 100.0% |

### `contrib/legacy`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`contrib.legacy`](modules/contrib.legacy.__init__.py.md) | Legacy module shims — deprecated scripts retained for compatibility. | 0 | 0 | 100.0% |
| [`contrib.legacy.lazy_http_bof`](modules/contrib.legacy.lazy_http_bof.py.md) |  | 0 | 2 | 0.0% |
| [`contrib.legacy.lazy_packet_image_sniffer`](modules/contrib.legacy.lazy_packet_image_sniffer.py.md) |  | 0 | 9 | 0.0% |
| [`contrib.legacy.lazyaddon_creator`](modules/contrib.legacy.lazyaddon_creator.py.md) | lazyaddon_creator.py ==================== Genera automáticamente un addon YAML de LazyOwn a partir de una URL de GitHub. | 0 | 14 | 93.3% |
| [`contrib.legacy.lazyarpspoofing`](modules/contrib.legacy.lazyarpspoofing.py.md) |  | 0 | 7 | 0.0% |
| [`contrib.legacy.lazybinenc`](modules/contrib.legacy.lazybinenc.py.md) |  | 0 | 2 | 0.0% |
| [`contrib.legacy.lazybotcli`](modules/contrib.legacy.lazybotcli.py.md) | main.py | 0 | 3 | 25.0% |
| [`contrib.legacy.lazybotnet`](modules/contrib.legacy.lazybotnet.py.md) | main.py | 1 | 15 | 5.9% |
| [`contrib.legacy.lazycam`](modules/contrib.legacy.lazycam.py.md) | This code is a portion of frigate Event Video Recorder (fEVR) Copyright (C) 2021-2022 The Bearded Tek (http://www.beardedtek.com) William Kenny This program is... | 1 | 7 | 11.1% |
| [`contrib.legacy.lazycreate_webshell`](modules/contrib.legacy.lazycreate_webshell.py.md) |  | 0 | 0 | 0.0% |
| [`contrib.legacy.lazydeepseekcli`](modules/contrib.legacy.lazydeepseekcli.py.md) | Unified Ollama/DeepSeek client for LazyOwn — merges lazydeepseekcli_local + lazydeepseekcli_localreport. | 0 | 10 | 9.1% |
| [`contrib.legacy.lazydisassebler`](modules/contrib.legacy.lazydisassebler.py.md) | disassembler.py | 1 | 7 | 100.0% |
| [`contrib.legacy.lazyftpsniff`](modules/contrib.legacy.lazyftpsniff.py.md) |  | 0 | 5 | 0.0% |
| [`contrib.legacy.lazygalazy`](modules/contrib.legacy.lazygalazy.py.md) |  | 1 | 6 | 0.0% |
| [`contrib.legacy.lazygptcli`](modules/contrib.legacy.lazygptcli.py.md) | main.py | 0 | 0 | 100.0% |
| [`contrib.legacy.lazygptcli_unified`](modules/contrib.legacy.lazygptcli_unified.py.md) | Unified Groq LLM client for LazyOwn — merges lazygptcli2/3/4/5 + lazyagentAi + lazygpttask + lazygptvulns + lazyredopgpt. | 0 | 8 | 100.0% |
| [`contrib.legacy.lazyhoneypot`](modules/contrib.legacy.lazyhoneypot.py.md) | main.py | 1 | 13 | 6.7% |
| [`contrib.legacy.lazyhttpreverseshell`](modules/contrib.legacy.lazyhttpreverseshell.py.md) |  | 0 | 7 | 0.0% |
| [`contrib.legacy.lazykeygen`](modules/contrib.legacy.lazykeygen.py.md) |  | 0 | 5 | 0.0% |
| [`contrib.legacy.lazylfi2rce`](modules/contrib.legacy.lazylfi2rce.py.md) |  | 0 | 4 | 0.0% |
| [`contrib.legacy.lazyllmchat`](modules/contrib.legacy.lazyllmchat.py.md) |  | 6 | 15 | 0.0% |
| [`contrib.legacy.lazylogpoisoning`](modules/contrib.legacy.lazylogpoisoning.py.md) |  | 0 | 3 | 0.0% |
| [`contrib.legacy.lazymariadb_rce_cve_2016-662`](modules/contrib.legacy.lazymariadb_rce_cve_2016-662.py.md) | MySQL / MariaDB / Percona - Remote Root Code Execution / PrivEsc PoC Exploit (CVE-2016-6662) 0ldSQL_MySQL_RCE_exploit.py (ver. | 0 | 3 | 25.0% |
| [`contrib.legacy.lazymidm`](modules/contrib.legacy.lazymidm.py.md) |  | 0 | 8 | 0.0% |
| [`contrib.legacy.lazymitmap`](modules/contrib.legacy.lazymitmap.py.md) |  | 0 | 19 | 80.0% |
| [`contrib.legacy.lazynetbios`](modules/contrib.legacy.lazynetbios.py.md) | main.py | 0 | 7 | 12.5% |
| [`contrib.legacy.lazyntlrelayx`](modules/contrib.legacy.lazyntlrelayx.py.md) |  | 0 | 2 | 0.0% |
| [`contrib.legacy.lazyopenssh77enum2`](modules/contrib.legacy.lazyopenssh77enum2.py.md) | CVE-2018-15473 SSH User Enumeration by Leap Security (@LeapSecurity) https://leapsecurity.io Credits: Matthew Daley, Justin Gardner, Lee David Painter | 1 | 4 | 16.7% |
| [`contrib.legacy.lazyphishingai`](modules/contrib.legacy.lazyphishingai.py.md) | main.py | 0 | 11 | 8.3% |
| [`contrib.legacy.lazyproxy`](modules/contrib.legacy.lazyproxy.py.md) |  | 0 | 9 | 0.0% |
| [`contrib.legacy.lazypwn`](modules/contrib.legacy.lazypwn.py.md) |  | 2 | 13 | 0.0% |
| [`contrib.legacy.lazypwnkit`](modules/contrib.legacy.lazypwnkit.py.md) |  | 0 | 5 | 66.7% |
| [`contrib.legacy.lazypyautogui`](modules/contrib.legacy.lazypyautogui.py.md) |  | 0 | 0 | 0.0% |
| [`contrib.legacy.lazyreversentlmv2`](modules/contrib.legacy.lazyreversentlmv2.py.md) |  | 0 | 2 | 0.0% |
| [`contrib.legacy.lazysearch`](modules/contrib.legacy.lazysearch.py.md) | main.py | 0 | 3 | 25.0% |
| [`contrib.legacy.lazysearch_bot`](modules/contrib.legacy.lazysearch_bot.py.md) | main.py | 0 | 13 | 7.1% |
| [`contrib.legacy.lazyseo`](modules/contrib.legacy.lazyseo.py.md) |  | 1 | 7 | 0.0% |
| [`contrib.legacy.lazysmbrelay`](modules/contrib.legacy.lazysmbrelay.py.md) |  | 1 | 6 | 0.0% |
| [`contrib.legacy.lazysniff`](modules/contrib.legacy.lazysniff.py.md) | main.py | 0 | 11 | 8.3% |
| [`contrib.legacy.lazysqli`](modules/contrib.legacy.lazysqli.py.md) | AUTHOR: jahman EDITED BY grisun0 | 0 | 4 | 20.0% |
| [`contrib.legacy.lazyssh`](modules/contrib.legacy.lazyssh.py.md) |  | 0 | 1 | 0.0% |
| [`contrib.legacy.lazyvsftp`](modules/contrib.legacy.lazyvsftp.py.md) |  | 0 | 3 | 0.0% |
| [`contrib.legacy.lazywerkzeug`](modules/contrib.legacy.lazywerkzeug.py.md) |  | 0 | 0 | 0.0% |
| [`contrib.legacy.sql`](modules/contrib.legacy.sql.py.md) |  | 0 | 3 | 0.0% |

### `core`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`core`](modules/core.__init__.py.md) | Core primitives for the LazyOwn framework. | 0 | 0 | 100.0% |
| [`core.api_authz`](modules/core.api_authz.py.md) | Tenant-bound API authorization for the LazyOwn C2 dashboard. | 3 | 16 | 65.0% |
| [`core.autonomous`](modules/core.autonomous.py.md) | Autonomous-run mode for the loop engine. | 0 | 2 | 100.0% |
| [`core.command_bridge`](modules/core.command_bridge.py.md) | Lightweight command execution bridge between C2 bots and the LazyOwn CLI shell. | 1 | 7 | 88.9% |
| [`core.config`](modules/core.config.py.md) | Configuration loader and Config wrapper. | 1 | 7 | 88.9% |
| [`core.console`](modules/core.console.py.md) | ANSI color constants and console output helpers. | 0 | 8 | 100.0% |
| [`core.credential_vault`](modules/core.credential_vault.py.md) | Credential vault — AES-256-GCM encryption for sensitive config values. | 0 | 7 | 100.0% |
| [`core.crypto`](modules/core.crypto.py.md) | Symmetric primitives used by the framework. | 0 | 5 | 100.0% |
| [`core.defaults`](modules/core.defaults.py.md) | Build-time default constants loaded from ``config/defaults.toml``. | 0 | 8 | 100.0% |
| [`core.dependencies`](modules/core.dependencies.py.md) | Graceful optional-import handling for heavy third-party dependencies. | 4 | 9 | 100.0% |
| [`core.error_advice`](modules/core.error_advice.py.md) | Actionable error advice with fix command and documentation link. | 2 | 3 | 100.0% |
| [`core.errors`](modules/core.errors.py.md) | Error taxonomy for the LazyOwn framework. | 11 | 11 | 56.5% |
| [`core.executor`](modules/core.executor.py.md) | Centralised subprocess wrapper for the LazyOwn framework. | 0 | 4 | 100.0% |
| [`core.hardening`](modules/core.hardening.py.md) | Centralized security hardening utilities for the LazyOwn framework. | 1 | 14 | 100.0% |
| [`core.host_policy`](modules/core.host_policy.py.md) | Single source of truth for host and network shape validation. | 0 | 3 | 100.0% |
| [`core.http`](modules/core.http.py.md) | HTTP and API utilities for the LazyOwn framework. | 0 | 10 | 100.0% |
| [`core.llm_budget`](modules/core.llm_budget.py.md) | LLM budget cap and per call token counter. | 9 | 24 | 82.4% |
| [`core.logging`](modules/core.logging.py.md) | Structured JSON-lines logging for the LazyOwn framework. | 2 | 4 | 85.7% |
| [`core.network`](modules/core.network.py.md) | Network primitives for the LazyOwn framework. | 0 | 8 | 100.0% |
| [`core.parsers`](modules/core.parsers.py.md) | Shared text kernel for the LazyOwn framework. | 0 | 1 | 100.0% |
| [`core.payload_schema`](modules/core.payload_schema.py.md) | Declarative schema and validation for ``payload.json``. | 4 | 7 | 100.0% |
| [`core.process`](modules/core.process.py.md) | Process and subprocess utilities for the LazyOwn framework. | 0 | 9 | 100.0% |
| [`core.profiles`](modules/core.profiles.py.md) | Runtime profiles: ``light`` vs ``full`` installations. | 0 | 3 | 100.0% |
| [`core.prompt`](modules/core.prompt.py.md) | Prompt builder for LazyOwn CLI and C2 dashboard banner. | 0 | 7 | 100.0% |
| [`core.protocols`](modules/core.protocols.py.md) | Stable structural interfaces (PEP 544 ``Protocol``) for high-level orchestration. | 5 | 7 | 76.9% |
| [`core.safe_console`](modules/core.safe_console.py.md) | Terminal-safe Rich console factory. | 0 | 5 | 100.0% |
| [`core.safe_exec`](modules/core.safe_exec.py.md) | Centralized safe command execution for the LazyOwn framework. | 2 | 9 | 100.0% |
| [`core.safe_import`](modules/core.safe_import.py.md) | Fail-closed import of attacker-supplied campaign packages. | 0 | 4 | 100.0% |
| [`core.safe_subprocess`](modules/core.safe_subprocess.py.md) | Safe subprocess runner for the LazyOwn framework. | 3 | 3 | 100.0% |
| [`core.scheduler`](modules/core.scheduler.py.md) | Centralized task scheduler for the LazyOwn framework. | 1 | 9 | 90.9% |
| [`core.security`](modules/core.security.py.md) | Security helpers for LazyOwn — anti-debug, certificate generation. | 0 | 2 | 100.0% |
| [`core.terminal_guard`](modules/core.terminal_guard.py.md) | Terminal state guard for interactive automation. | 1 | 6 | 100.0% |
| [`core.text_utils`](modules/core.text_utils.py.md) | Shared text helpers for terminal surfaces. | 0 | 1 | 100.0% |
| [`core.validators`](modules/core.validators.py.md) | Input validators for runtime configuration values. | 0 | 4 | 100.0% |

### `deploy/range/ad-mini`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`deploy.range.ad-mini.traffic-gen`](modules/deploy.range.ad-mini.traffic-gen.py.md) | Fake network traffic generator for the AD mini range. | 0 | 1 | 100.0% |

### `lazyc2`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazyc2`](modules/lazyc2.__init__.py.md) |  | 0 | 0 | 0.0% |
| [`lazyc2.addon_creator`](modules/lazyc2.addon_creator.py.md) | LazyAddon creator contract for the LazyOwn C2 web interface. | 8 | 17 | 96.2% |
| [`lazyc2.app_factory`](modules/lazyc2.app_factory.py.md) | Flask application factory for the LazyOwn C2 server. | 0 | 1 | 100.0% |
| [`lazyc2.models`](modules/lazyc2.models.py.md) | C2 data models extracted from lazyc2.py. | 1 | 1 | 33.3% |
| [`lazyc2.state`](modules/lazyc2.state.py.md) | Global C2 server state — namespace for shared mutable objects. | 0 | 0 | 100.0% |

### `lazyc2/blueprints`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazyc2.blueprints`](modules/lazyc2.blueprints.__init__.py.md) | Flask Blueprints for lazydown C2. | 0 | 0 | 100.0% |
| [`lazyc2.blueprints.addons`](modules/lazyc2.blueprints.addons.py.md) | LazyAddon creator blueprint for the C2 dashboard. | 0 | 6 | 100.0% |
| [`lazyc2.blueprints.api`](modules/lazyc2.blueprints.api.py.md) | API blueprint for the LazyOwn C2 server. | 1 | 6 | 100.0% |
| [`lazyc2.blueprints.api_v1`](modules/lazyc2.blueprints.api_v1.py.md) | Versioned REST API (``/api/v1``) for the LazyOwn C2 server. | 0 | 7 | 100.0% |
| [`lazyc2.blueprints.auth`](modules/lazyc2.blueprints.auth.py.md) | Authentication and authorisation blueprint for the LazyOwn C2 server. | 0 | 14 | 6.7% |
| [`lazyc2.blueprints.beacon`](modules/lazyc2.blueprints.beacon.py.md) | Beacon communication blueprint for the LazyOwn C2 server. | 0 | 4 | 100.0% |
| [`lazyc2.blueprints.operations`](modules/lazyc2.blueprints.operations.py.md) | Operations blueprint — tasks, CVEs, notes, and event management. | 0 | 13 | 100.0% |
| [`lazyc2.blueprints.phishing`](modules/lazyc2.blueprints.phishing.py.md) | Phishing blueprint for the LazyOwn C2 server. | 0 | 6 | 100.0% |
| [`lazyc2.blueprints.session_auth`](modules/lazyc2.blueprints.session_auth.py.md) | Session-based authentication gate for operator dashboard blueprints. | 0 | 1 | 100.0% |

### `lazyc2/extensions`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazyc2.extensions`](modules/lazyc2.extensions.__init__.py.md) | Shared C2 extension modules. | 0 | 0 | 100.0% |
| [`lazyc2.extensions.decoy`](modules/lazyc2.extensions.decoy.py.md) | Decoy / honeypot page for unauthenticated visitors. | 0 | 1 | 100.0% |
| [`lazyc2.extensions.short_urls`](modules/lazyc2.extensions.short_urls.py.md) | Short URL management utilities for the C2 phishing module. | 0 | 4 | 100.0% |
| [`lazyc2.extensions.storage`](modules/lazyc2.extensions.storage.py.md) | JSON-file storage helpers for the C2 web interface. | 0 | 12 | 100.0% |
| [`lazyc2.extensions.users`](modules/lazyc2.extensions.users.py.md) | User management utilities for the C2 auth module. | 0 | 3 | 100.0% |

### `lazyc2/security`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazyc2.security`](modules/lazyc2.security.__init__.py.md) |  | 0 | 0 | 0.0% |
| [`lazyc2.security.command_allowlist`](modules/lazyc2.security.command_allowlist.py.md) | Command allowlist policy for the LazyOwn C2 ``/api/run`` endpoint. | 3 | 4 | 100.0% |
| [`lazyc2.security.constants`](modules/lazyc2.security.constants.py.md) | Security constants and validation patterns for the LazyOwn C2 web layer. | 0 | 0 | 100.0% |
| [`lazyc2.security.cors`](modules/lazyc2.security.cors.py.md) | CORS origin allowlist policy for the LazyOwn C2 web layer. | 2 | 5 | 100.0% |
| [`lazyc2.security.csrf`](modules/lazyc2.security.csrf.py.md) | CSRF protection policy for the LazyOwn C2 web layer. | 1 | 10 | 100.0% |
| [`lazyc2.security.html_sanitizer`](modules/lazyc2.security.html_sanitizer.py.md) | HTML sanitizer backed by ``bleach`` for the LazyOwn C2 web layer. | 0 | 1 | 100.0% |
| [`lazyc2.security.https_redirect`](modules/lazyc2.security.https_redirect.py.md) | HTTPS redirect policy for the LazyOwn C2 web layer. | 2 | 3 | 100.0% |
| [`lazyc2.security.services`](modules/lazyc2.security.services.py.md) | Security services for the LazyOwn C2 web layer. | 4 | 11 | 75.0% |
| [`lazyc2.security.trusted_proxy`](modules/lazyc2.security.trusted_proxy.py.md) | Trusted proxy resolver for the LazyOwn C2 web layer. | 1 | 4 | 100.0% |
| [`lazyc2.security.validators`](modules/lazyc2.security.validators.py.md) | Input validators for the LazyOwn C2 web layer. | 0 | 9 | 100.0% |

### `lazygui`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazygui`](modules/lazygui.__init__.py.md) | LazyOwn Operator Console. | 0 | 0 | 100.0% |
| [`lazygui.__main__`](modules/lazygui.__main__.py.md) | Entry point for ``python -m lazygui``. | 0 | 1 | 100.0% |
| [`lazygui.app`](modules/lazygui.app.py.md) | Application bootstrap. | 1 | 3 | 100.0% |
| [`lazygui.version`](modules/lazygui.version.py.md) | Single source of truth for the package version string. | 0 | 0 | 100.0% |

### `lazygui/config`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazygui.config`](modules/lazygui.config.__init__.py.md) | Configuration layer. | 0 | 0 | 100.0% |
| [`lazygui.config.c2_credentials`](modules/lazygui.config.c2_credentials.py.md) | C2 auto-generated credentials discovery. | 1 | 3 | 100.0% |
| [`lazygui.config.constants`](modules/lazygui.config.constants.py.md) | Immutable application constants. | 13 | 1 | 100.0% |
| [`lazygui.config.paths`](modules/lazygui.config.paths.py.md) | Filesystem layout resolver. | 1 | 8 | 100.0% |
| [`lazygui.config.settings`](modules/lazygui.config.settings.py.md) | Persisted user settings. | 1 | 17 | 53.8% |

### `lazygui/panels`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazygui.panels`](modules/lazygui.panels.__init__.py.md) | Dockable panels assembled from the reusable widgets. | 0 | 0 | 100.0% |
| [`lazygui.panels.base`](modules/lazygui.panels.base.py.md) | Common :class:`QDockWidget` base for every panel. | 1 | 3 | 100.0% |
| [`lazygui.panels.campaign_panel`](modules/lazygui.panels.campaign_panel.py.md) | Campaign management panel for the operator console. | 1 | 2 | 100.0% |
| [`lazygui.panels.credentials_panel`](modules/lazygui.panels.credentials_panel.py.md) | Credentials and loot panel for the operator console. | 1 | 1 | 100.0% |
| [`lazygui.panels.cve_panel`](modules/lazygui.panels.cve_panel.py.md) | CVE tracker panel for the operator console. | 1 | 2 | 100.0% |
| [`lazygui.panels.event_log_panel`](modules/lazygui.panels.event_log_panel.py.md) | Panel hosting the application-wide event log. | 1 | 1 | 100.0% |
| [`lazygui.panels.graph_panel`](modules/lazygui.panels.graph_panel.py.md) | Graph panel for Cobalt Strike-style attack topography visualization. | 1 | 2 | 100.0% |
| [`lazygui.panels.history_panel`](modules/lazygui.panels.history_panel.py.md) | Command history panel showing beacon command logs. | 1 | 1 | 100.0% |
| [`lazygui.panels.killchain_panel`](modules/lazygui.panels.killchain_panel.py.md) | Kill-chain visualization panel for the operator console. | 1 | 1 | 100.0% |
| [`lazygui.panels.listeners_panel`](modules/lazygui.panels.listeners_panel.py.md) | Panel that lists the listeners advertised by the backend. | 1 | 1 | 100.0% |
| [`lazygui.panels.marketplace_panel`](modules/lazygui.panels.marketplace_panel.py.md) | Marketplace panel for YARA rules, Nuclei templates, YAML addons and Lua plugins. | 1 | 1 | 100.0% |
| [`lazygui.panels.registry`](modules/lazygui.panels.registry.py.md) | Registry that owns all dock panels. | 1 | 4 | 100.0% |
| [`lazygui.panels.sessions_panel`](modules/lazygui.panels.sessions_panel.py.md) | Panel that lists active sessions reported by the backend. | 1 | 1 | 100.0% |
| [`lazygui.panels.terminal_panel`](modules/lazygui.panels.terminal_panel.py.md) | Console panel hosting the :class:`TerminalView` with beacon command support. | 1 | 3 | 100.0% |

### `lazygui/services`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazygui.services`](modules/lazygui.services.__init__.py.md) | Service layer. | 0 | 0 | 100.0% |
| [`lazygui.services.backend`](modules/lazygui.services.backend.py.md) | Backend abstraction. | 3 | 16 | 100.0% |
| [`lazygui.services.event_log`](modules/lazygui.services.event_log.py.md) | In-memory ring buffer for :class:`EventRecord`. | 1 | 6 | 100.0% |
| [`lazygui.services.factory`](modules/lazygui.services.factory.py.md) | Factory for backend instances. | 1 | 3 | 100.0% |
| [`lazygui.services.local_backend`](modules/lazygui.services.local_backend.py.md) | Local backend that runs the LazyOwn cmd2 console on a PTY. | 1 | 10 | 100.0% |
| [`lazygui.services.models`](modules/lazygui.services.models.py.md) | Immutable domain types consumed by the UI. | 12 | 3 | 100.0% |
| [`lazygui.services.teamserver_backend`](modules/lazygui.services.teamserver_backend.py.md) | Teamserver backend with Socket.IO real-time and full HTTP API coverage. | 2 | 14 | 100.0% |

### `lazygui/theme`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazygui.theme`](modules/lazygui.theme.__init__.py.md) | Theme subsystem. | 0 | 0 | 100.0% |
| [`lazygui.theme.manager`](modules/lazygui.theme.manager.py.md) | Theme registry and runtime application of stylesheets. | 1 | 7 | 100.0% |
| [`lazygui.theme.qss_builder`](modules/lazygui.theme.qss_builder.py.md) | Builds a Qt stylesheet string from :class:`ThemeTokens`. | 1 | 1 | 100.0% |
| [`lazygui.theme.tokens`](modules/lazygui.theme.tokens.py.md) | Design tokens describing a single theme. | 1 | 0 | 100.0% |

### `lazygui/theme/palettes`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazygui.theme.palettes`](modules/lazygui.theme.palettes.__init__.py.md) | Built-in palette registry. | 0 | 1 | 100.0% |
| [`lazygui.theme.palettes.catppuccin_mocha`](modules/lazygui.theme.palettes.catppuccin_mocha.py.md) | Catppuccin Mocha palette - warm pastel dark theme. | 0 | 0 | 100.0% |
| [`lazygui.theme.palettes.cobalt_clone`](modules/lazygui.theme.palettes.cobalt_clone.py.md) | Cobalt Clone palette - homage to the classic command-and-control look. | 0 | 0 | 100.0% |
| [`lazygui.theme.palettes.gruvbox_dark`](modules/lazygui.theme.palettes.gruvbox_dark.py.md) | Gruvbox Dark palette - retro warm contrast theme. | 0 | 0 | 100.0% |
| [`lazygui.theme.palettes.solarized_light`](modules/lazygui.theme.palettes.solarized_light.py.md) | Solarized Light palette - low-contrast daylight option. | 0 | 0 | 100.0% |
| [`lazygui.theme.palettes.tactical_green`](modules/lazygui.theme.palettes.tactical_green.py.md) | Tactical Green palette - the LazyOwn signature look. | 0 | 0 | 100.0% |
| [`lazygui.theme.palettes.tokyo_night`](modules/lazygui.theme.palettes.tokyo_night.py.md) | Tokyo Night palette - balanced dark blue theme. | 0 | 0 | 100.0% |

### `lazygui/widgets`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazygui.widgets`](modules/lazygui.widgets.__init__.py.md) | Reusable widgets. | 0 | 0 | 100.0% |
| [`lazygui.widgets.beacon_command_modal`](modules/lazygui.widgets.beacon_command_modal.py.md) | Beacon command modal — send commands to beacons and inspect full history. | 1 | 3 | 100.0% |
| [`lazygui.widgets.command_palette_list`](modules/lazygui.widgets.command_palette_list.py.md) | Result list and action model for the command palette. | 2 | 4 | 100.0% |
| [`lazygui.widgets.event_log_view`](modules/lazygui.widgets.event_log_view.py.md) | Read-only viewer for :class:`EventLog` records. | 1 | 3 | 100.0% |
| [`lazygui.widgets.filter_bar`](modules/lazygui.widgets.filter_bar.py.md) | Reusable text-filter bar with debounced ``filter_changed`` signal. | 1 | 3 | 100.0% |
| [`lazygui.widgets.graph_view`](modules/lazygui.widgets.graph_view.py.md) | Interactive attack topography graph widget. | 5 | 22 | 60.7% |
| [`lazygui.widgets.status_badge`](modules/lazygui.widgets.status_badge.py.md) | Compact label that reflects a :class:`BackendStatus` value. | 1 | 2 | 100.0% |
| [`lazygui.widgets.terminal_view`](modules/lazygui.widgets.terminal_view.py.md) | ANSI-aware terminal viewer. | 1 | 3 | 100.0% |

### `lazygui/windows`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazygui.windows`](modules/lazygui.windows.__init__.py.md) | Top-level windows and dialogs. | 0 | 0 | 100.0% |
| [`lazygui.windows.command_palette_window`](modules/lazygui.windows.command_palette_window.py.md) | Frameless palette window invoked by ``Ctrl+K``. | 1 | 4 | 100.0% |
| [`lazygui.windows.connect_dialog`](modules/lazygui.windows.connect_dialog.py.md) | Connection dialog for picking a backend. | 2 | 3 | 100.0% |
| [`lazygui.windows.main_window`](modules/lazygui.windows.main_window.py.md) | Operator console main window. | 1 | 5 | 100.0% |

### `lazyown-docker`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`lazyown-docker/entrypoint.sh`](modules/lazyown-docker.entrypoint.sh.md) | LazyOwn Entrypoint Script Initializes LazyOwn framework in a Docker container with tmux sessions | 0 | 0 | 100.0% |
| [`lazyown-docker/hostdiscover.sh`](modules/lazyown-docker.hostdiscover.sh.md) |  | 0 | 2 | 0.0% |
| [`lazyown-docker/init.sh`](modules/lazyown-docker.init.sh.md) |  | 0 | 0 | 0.0% |
| [`lazyown-docker/mkdocker.sh`](modules/lazyown-docker.mkdocker.sh.md) | LazyOwn Dockerizer Script Builds, runs, and manages Docker containers for LazyOwn red teaming framework | 0 | 12 | 100.0% |

### `modules`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`modules.49803`](modules/modules.49803.py.md) | Exploit Title: OpenPLC 3 - Remote Code Execution (Authenticated) Date: 25/04/2021 Exploit Author: Fellipe Oliveira Vendor Homepage... | 0 | 3 | 25.0% |
| [`modules/CVE-2018-15133.php`](modules/modules.CVE-2018-15133.php.md) |  | 0 | 0 | 0.0% |
| [`modules.CVE-2023-28432`](modules/modules.CVE-2023-28432.py.md) |  | 0 | 1 | 0.0% |
| [`modules.LazyOwnExplorer`](modules/modules.LazyOwnExplorer.py.md) | main.py | 2 | 18 | 4.8% |
| [`modules`](modules/modules.__init__.py.md) |  | 0 | 0 | 0.0% |
| [`modules.adcs_attacks`](modules/modules.adcs_attacks.py.md) | Active Directory Certificate Services (AD CS) attack module. | 2 | 8 | 100.0% |
| [`modules.agent_runner`](modules/modules.agent_runner.py.md) | LazyOwn AI Agent - Ultimate Edition Mejoras: Anti-Hang (Timeout), Gestión de Memoria, Validación de Argumentos y Anti-Loop. | 6 | 19 | 30.8% |
| [`modules.ai_exploit_chain`](modules/modules.ai_exploit_chain.py.md) | AI-Driven Exploit Chaining Engine. | 2 | 7 | 90.0% |
| [`modules.ai_fallback`](modules/modules.ai_fallback.py.md) | LazyOwn AI Fallback Chain ========================== Unified LLM caller with automatic fallback: | 1 | 1 | 66.7% |
| [`modules.ai_model`](modules/modules.ai_model.py.md) | Concrete language model backends for LazyOwn. | 6 | 22 | 82.8% |
| [`modules/amsi.c`](modules/modules.amsi.c.md) | ¡Gracias a Saad! | 0 | 10 | 81.8% |
| [`modules.amt_auth_bypass`](modules/modules.amt_auth_bypass.py.md) |  | 1 | 2 | 0.0% |
| [`modules.apt_playbooks`](modules/modules.apt_playbooks.py.md) | APT Playbook Engine — map public APT reports to executable Atomic Red Team chains. | 5 | 8 | 35.7% |
| [`modules.asset_graph`](modules/modules.asset_graph.py.md) | Global asset truth store joined to per-task exploration chains. | 5 | 12 | 100.0% |
| [`modules.atomic_enricher`](modules/modules.atomic_enricher.py.md) | atomic_enricher.py — Enrich techniques.parquet with structured derived columns. | 0 | 3 | 100.0% |
| [`modules.attack_surface3d`](modules/modules.attack_surface3d.py.md) | Attack-surface 3D intel module: C2-centred campaign graph. | 0 | 2 | 100.0% |
| [`modules.auto_pivot`](modules/modules.auto_pivot.py.md) | Auto-Pivoting Engine for LazyOwn. | 3 | 17 | 9.5% |
| [`modules.auto_purple`](modules/modules.auto_purple.py.md) | Purple Team Closed-Loop — honest measurement of offensive detection. | 6 | 19 | 57.7% |
| [`modules.auto_registry`](modules/modules.auto_registry.py.md) | Registry of loop-ready automation verbs (the ``auto_*`` family). | 2 | 22 | 100.0% |
| [`modules.autonomous_exploit_engine`](modules/modules.autonomous_exploit_engine.py.md) | Autonomous Exploitation Engine — AI-powered self-adapting exploit chainer. | 4 | 12 | 88.2% |
| [`modules.aws_attacks`](modules/modules.aws_attacks.py.md) | AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. | 2 | 9 | 83.3% |
| [`modules.beacon_config_builder`](modules/modules.beacon_config_builder.py.md) | Beacon configuration builder — wires profile engines into beacon compile-time config. | 2 | 9 | 91.7% |
| [`modules.beacon_history`](modules/modules.beacon_history.py.md) | Persistent beacon command/result history storage. | 1 | 6 | 100.0% |
| [`modules.bin2img`](modules/modules.bin2img.py.md) |  | 0 | 2 | 0.0% |
| [`modules.bitm_engine`](modules/modules.bitm_engine.py.md) | Browser-in-the-Middle (BitM) attack engine. | 1 | 6 | 100.0% |
| [`modules.bof_registry`](modules/modules.bof_registry.py.md) | Beacon Object File (BOF) registry and marketplace for LazyOwn. | 7 | 33 | 95.1% |
| [`modules.c2_builder`](modules/modules.c2_builder.py.md) | C2 agent builder with profile-driven compilation and safe templating. | 2 | 2 | 80.0% |
| [`modules.c2_messaging_base`](modules/modules.c2_messaging_base.py.md) |  | 2 | 10 | 84.6% |
| [`modules.c2_profile`](modules/modules.c2_profile.py.md) | modules/c2_profile.py ====================== Malleable C2 profile system for LazyOwn. | 8 | 19 | 92.9% |
| [`modules.c2_profile_engine`](modules/modules.c2_profile_engine.py.md) | Extended malleable C2 profile engine with TLS, DNS, SMB, and WebSocket transports. | 9 | 37 | 95.7% |
| [`modules/cal.sh`](modules/modules.cal.sh.md) |  | 0 | 3 | 75.0% |
| [`modules.categories`](modules/modules.categories.py.md) | modules/categories.py ===================== cmd2 command category strings for LazyOwn. | 0 | 0 | 100.0% |
| [`modules.cicd_enumerator`](modules/modules.cicd_enumerator.py.md) | CI/CD Pipeline Enumeration Module. | 2 | 5 | 87.5% |
| [`modules.cli_auth`](modules/modules.cli_auth.py.md) | CLI authentication module — login against users.json with remember-me. | 0 | 10 | 100.0% |
| [`modules.cloud_enum`](modules/modules.cloud_enum.py.md) | Native cloud enumeration modules for AWS, Azure, and GCP. | 1 | 6 | 100.0% |
| [`modules.collab_bp`](modules/modules.collab_bp.py.md) | modules/collab_bp.py ==================== Multi-operator collaboration layer for LazyOwn. | 6 | 31 | 13.2% |
| [`modules.colors`](modules/modules.colors.py.md) |  | 0 | 3 | 25.0% |
| [`modules.command_executor`](modules/modules.command_executor.py.md) | UnifiedCommandExecutor — shared shell command execution service. | 2 | 14 | 76.5% |
| [`modules.compliance`](modules/modules.compliance.py.md) | modules/compliance.py ===================== Enterprise compliance engine for LazyOwn RedTeam Framework. | 4 | 14 | 42.1% |
| [`modules.conditional_hooks`](modules/modules.conditional_hooks.py.md) | Conditional Hooks System for LazyOwn (Mythic-style triggers). | 2 | 15 | 77.8% |
| [`modules.config_store`](modules/modules.config_store.py.md) | Thread-safe singleton facade over core.config for payload.json. | 0 | 6 | 100.0% |
| [`modules.credential_reuse`](modules/modules.credential_reuse.py.md) | Credential Reuse Engine for LazyOwn. | 2 | 9 | 83.3% |
| [`modules.cross_cloud`](modules/modules.cross_cloud.py.md) | Cross-cloud identity paths — multi-cloud identity federation abuse. | 2 | 8 | 81.8% |
| [`modules.custom_tools`](modules/modules.custom_tools.py.md) | Operator-defined custom tools exposed to the autonomous loop. | 0 | 6 | 100.0% |
| [`modules.cve_matcher`](modules/modules.cve_matcher.py.md) | modules/cve_matcher.py ======================= CVE lookup via NVD API 2.0 (no key required for basic queries). | 2 | 5 | 87.5% |
| [`modules.dacl_abuse`](modules/modules.dacl_abuse.py.md) | DACL/SACL abuse module — ACL manipulation for AD privilege escalation. | 3 | 8 | 91.7% |
| [`modules.dashboard_bp`](modules/modules.dashboard_bp.py.md) | modules/dashboard_bp.py ======================== Real-time SOC dashboard as a Flask Blueprint. | 0 | 4 | 100.0% |
| [`modules.dashboard_engine`](modules/modules.dashboard_engine.py.md) | Live Network Map Dashboard for LazyOwn. | 3 | 11 | 53.3% |
| [`modules.db`](modules/modules.db.py.md) | SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes. | 1 | 29 | 100.0% |
| [`modules.delegation_attacks`](modules/modules.delegation_attacks.py.md) | Active Directory delegation enumeration and abuse. | 3 | 9 | 92.3% |
| [`modules.detailed_search`](modules/modules.detailed_search.py.md) | main.py | 0 | 1 | 50.0% |
| [`modules.detection_feed`](modules/modules.detection_feed.py.md) | Dynamic detection feed for the Detection Oracle. | 2 | 5 | 87.5% |
| [`modules.detection_oracle`](modules/modules.detection_oracle.py.md) | modules/detection_oracle.py ============================ Blue Team Mirror — predicts detection probability for a given action before it is executed by the... | 4 | 9 | 92.9% |
| [`modules.dns_beacon`](modules/modules.dns_beacon.py.md) | DNS Beacon — covert C2 channel via DNS tunneling. | 2 | 10 | 100.0% |
| [`modules.domain_dominance`](modules/modules.domain_dominance.py.md) | Domain Dominance Engine — automated Active Directory takeover. | 4 | 7 | 83.3% |
| [`modules.dotnet_payload`](modules/modules.dotnet_payload.py.md) | .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. | 2 | 8 | 90.9% |
| [`modules.dpapi_harvester`](modules/modules.dpapi_harvester.py.md) | DPAPI credential decryption and harvesting engine. | 3 | 4 | 75.0% |
| [`modules/duckdns.sh`](modules/modules.duckdns.sh.md) | Solicita el TOKEN y el DOMAIN al usuario | 0 | 0 | 100.0% |
| [`modules.edr_detector`](modules/modules.edr_detector.py.md) | EDR/AV Detection and Evasion Profiling Engine. | 3 | 3 | 71.4% |
| [`modules/eegg.sh`](modules/modules.eegg.sh.md) | Definición de colores | 0 | 4 | 80.0% |
| [`modules.engage_summary`](modules/modules.engage_summary.py.md) | Rich per-step engagement summaries from evidence and sessions artefacts. | 0 | 8 | 100.0% |
| [`modules.engagement_hooks`](modules/modules.engagement_hooks.py.md) | modules/engagement_hooks.py — Engagement narration and notification fabric ========================================================================== | 8 | 22 | 87.1% |
| [`modules.enrich`](modules/modules.enrich.py.md) | Async target enrichment with scan dedup (LAZY enrich parity). | 2 | 8 | 100.0% |
| [`modules.entra_id_attacks`](modules/modules.entra_id_attacks.py.md) | Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing. | 2 | 10 | 84.6% |
| [`modules.estorides_fusion`](modules/modules.estorides_fusion.py.md) | Estorides intel fusion: merge OSINT graph entities into campaign graphs. | 0 | 9 | 100.0% |
| [`modules.estorides_importer`](modules/modules.estorides_importer.py.md) | estorides_importer ================== Bidirectional bridge between Estorides (passive OSINT) and LazyOwn (active pentest). | 8 | 34 | 65.1% |
| [`modules.evasion_engine`](modules/modules.evasion_engine.py.md) | Advanced Evasion Engine for LazyOwn C2 operations. | 3 | 9 | 15.4% |
| [`modules.evasive_payloads`](modules/modules.evasive_payloads.py.md) | Advanced evasive payload generation with multiple obfuscation strategies. | 1 | 9 | 90.9% |
| [`modules.event_bus`](modules/modules.event_bus.py.md) | UnifiedEventBus — central nervous system connecting all LazyOwn components. | 8 | 27 | 52.8% |
| [`modules.event_consumers`](modules/modules.event_consumers.py.md) | Event Consumers — reactive layer that makes EventBus events drive real actions. | 5 | 9 | 53.3% |
| [`modules.event_engine`](modules/modules.event_engine.py.md) | LazyOwn Event Engine ==================== Tails sessions/LazyOwn_session_report.csv for new command executions, matches them against rules in... | 0 | 6 | 85.7% |
| [`modules.evidence`](modules/modules.evidence.py.md) | Content-addressed evidence vault independent of disposable traffic. | 2 | 7 | 100.0% |
| [`modules/evilhttprev.sh`](modules/modules.evilhttprev.sh.md) |  | 0 | 0 | 0.0% |
| [`modules/exp.c`](modules/modules.exp.c.md) |  | 9 | 45 | 1.8% |
| [`modules.exploit_chain`](modules/modules.exploit_chain.py.md) | Autonomous exploitation chain engine. | 5 | 7 | 92.3% |
| [`modules.exploit_recommender`](modules/modules.exploit_recommender.py.md) | AI-Powered Exploit Recommendation Engine for LazyOwn. | 2 | 7 | 60.0% |
| [`modules.exploitgym_gym`](modules/modules.exploitgym_gym.py.md) | ExploitGym integration — real-world vulnerability-to-exploit benchmark. | 0 | 7 | 100.0% |
| [`modules/fast_run_service.sh`](modules/modules.fast_run_service.sh.md) | fast_run_service.sh LazyOwn service-mode orchestrator. | 0 | 39 | 25.0% |
| [`modules.finding_lifecycle`](modules/modules.finding_lifecycle.py.md) | Finding confirmation lifecycle: pending -> confirmed / rejected. | 2 | 15 | 100.0% |
| [`modules.forensic_cleaner`](modules/modules.forensic_cleaner.py.md) | Forensic artifact cleaner — Prefetch, Shimcache, Amcache, MFT/USN cleanup. | 2 | 6 | 88.9% |
| [`modules.gcp_attacks`](modules/modules.gcp_attacks.py.md) | GCP privilege escalation — service account impersonation, Cloud Functions, GCS enumeration. | 2 | 9 | 83.3% |
| [`modules.generate_tools`](modules/modules.generate_tools.py.md) | generate_tools.py | 0 | 1 | 50.0% |
| [`modules.goals`](modules/modules.goals.py.md) | Goal decomposition round-0 with constraints and proof. | 3 | 10 | 100.0% |
| [`modules.gpo_abuse`](modules/modules.gpo_abuse.py.md) | GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation. | 3 | 13 | 94.1% |
| [`modules/gui_askpass.sh`](modules/modules.gui_askpass.sh.md) | gui_askpass.sh — SUDO_ASKPASS helper for LazyOwn MCP Used by: sudo -A <script> (set SUDO_ASKPASS to this file's path) Tries GUI backends in order of preference. | 0 | 5 | 33.3% |
| [`modules.hash_cracker`](modules/modules.hash_cracker.py.md) | Hash cracking pipeline — John the Ripper and Hashcat integration. | 3 | 7 | 72.7% |
| [`modules.hive_invoke`](modules/modules.hive_invoke.py.md) | modules/hive_invoke.py ======================= Invokes Claude Code CLI with the LazyOwn MCP server and forwards an operator prompt for autonomous or hive-mind... | 0 | 1 | 50.0% |
| [`modules/hostdiscover.sh`](modules/modules.hostdiscover.sh.md) |  | 0 | 2 | 0.0% |
| [`modules.ia_code_analysis`](modules/modules.ia_code_analysis.py.md) |  | 1 | 7 | 66.7% |
| [`modules.ia_logs_analysis`](modules/modules.ia_logs_analysis.py.md) | log_monitor_bot.py | 1 | 6 | 75.0% |
| [`modules.ia_network_analysis`](modules/modules.ia_network_analysis.py.md) | ia_network_analysis.py | 0 | 4 | 80.0% |
| [`modules.icmp_client`](modules/modules.icmp_client.py.md) |  | 0 | 7 | 25.0% |
| [`modules.icmp_server`](modules/modules.icmp_server.py.md) |  | 0 | 9 | 20.0% |
| [`modules.img2bin`](modules/modules.img2bin.py.md) |  | 0 | 2 | 0.0% |
| [`modules.intel_fusion`](modules/modules.intel_fusion.py.md) | Sessions attack-intel fusion: data -> information -> intelligence. | 0 | 9 | 100.0% |
| [`modules.intelligence_engine`](modules/modules.intelligence_engine.py.md) | IntelligenceEngine — unified collection→analysis→intelligence pipeline. | 5 | 14 | 95.0% |
| [`modules.intercept`](modules/modules.intercept.py.md) | User-configurable tool-call interception layer with human-in-loop approvals. | 7 | 20 | 100.0% |
| [`modules/internal_discover.sh`](modules/modules.internal_discover.sh.md) |  | 0 | 0 | 0.0% |
| [`modules/iptables_portforward.sh`](modules/modules.iptables_portforward.sh.md) | ------------------------------------------------------------------------------- iptables-port-forward.sh This script configures port forwarding using iptables. | 0 | 1 | 100.0% |
| [`modules.jsonl_tail`](modules/modules.jsonl_tail.py.md) | Incremental JSONL reader shared by the monitor TUI and the loop runner. | 1 | 2 | 100.0% |
| [`modules.jwtexploit`](modules/modules.jwtexploit.py.md) |  | 0 | 0 | 0.0% |
| [`modules.k8s_attacks`](modules/modules.k8s_attacks.py.md) | Kubernetes attack module — RBAC enumeration, pod escape, etcd access, Helm abuse. | 2 | 9 | 83.3% |
| [`modules.kerberoasting`](modules/modules.kerberoasting.py.md) | Advanced Kerberoasting — targeted SPN enumeration, AES-only attacks, hashcat integration. | 3 | 11 | 93.3% |
| [`modules.kerberos_core`](modules/modules.kerberos_core.py.md) | Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. | 10 | 20 | 87.1% |
| [`modules.kerberos_tickets`](modules/modules.kerberos_tickets.py.md) | Kerberos ticket forgery attacks — silver, golden, diamond, sapphire tickets. | 8 | 12 | 81.0% |
| [`modules.kill_chain_viz`](modules/modules.kill_chain_viz.py.md) | SVG / HTML kill-chain visualizer — generates standalone HTML with embedded SVG. | 0 | 2 | 33.3% |
| [`modules.killchain`](modules/modules.killchain.py.md) | Unified kill-chain — single source of truth consumed by all surfaces. | 3 | 18 | 100.0% |
| [`modules.kivi`](modules/modules.kivi.py.md) |  | 1 | 2 | 0.0% |
| [`modules.lazy_agent`](modules/modules.lazy_agent.py.md) | Agentic tool-calling bridge for the loop and the main agent. | 2 | 16 | 100.0% |
| [`modules.lazy_bridge`](modules/modules.lazy_bridge.py.md) | Bidirectional LAZY <-> LazyOwn bridge. | 0 | 14 | 100.0% |
| [`modules.lazy_cli_bridge`](modules/modules.lazy_cli_bridge.py.md) | Full CLI catalog for the Lazy autonomous loop. | 0 | 10 | 100.0% |
| [`modules.lazy_engine`](modules/modules.lazy_engine.py.md) | Lazy autonomous loop engine: single orchestrator for lazy_* commands. | 1 | 0 | 100.0% |
| [`modules.lazy_installer`](modules/modules.lazy_installer.py.md) | Capability installer for the Lazy autonomous loop. | 0 | 6 | 100.0% |
| [`modules.lazy_intel`](modules/modules.lazy_intel.py.md) | Intel feed from the Lazy autonomous loop. | 0 | 9 | 100.0% |
| [`modules.lazy_loop`](modules/modules.lazy_loop.py.md) | Lazy autonomous loop for LazyOwn. | 29 | 261 | 100.0% |
| [`modules.lazy_mentions`](modules/modules.lazy_mentions.py.md) | LAZY chat mentions with multi-type search and scroll pagination. | 3 | 3 | 100.0% |
| [`modules.lazy_orchestrator_feedback`](modules/modules.lazy_orchestrator_feedback.py.md) | Organic orchestrator training from loop usage. | 0 | 5 | 100.0% |
| [`modules.lazy_proxy`](modules/modules.lazy_proxy.py.md) | Recording HTTP/HTTPS proxy for the autonomous loop. | 2 | 17 | 100.0% |
| [`modules.lazy_rbac`](modules/modules.lazy_rbac.py.md) | modules/lazy_rbac.py ==================== Role-Based Access Control, Multi-Factor Authentication, and Multi-Tenancy for the LazyOwn RedTeam Framework. | 6 | 48 | 20.0% |
| [`modules.lazy_roles`](modules/modules.lazy_roles.py.md) | Lazy specialist roles for the autonomous loop. | 0 | 4 | 100.0% |
| [`modules.lazy_runner`](modules/modules.lazy_runner.py.md) | Single execution path for ``lazy_loop`` and ``auto_loop``. | 1 | 5 | 100.0% |
| [`modules.lazy_sandbox`](modules/modules.lazy_sandbox.py.md) | Per-task Docker sandbox for the Lazy autonomous loop. | 0 | 10 | 100.0% |
| [`modules.lazy_skill_mirror`](modules/modules.lazy_skill_mirror.py.md) | Mirror LazyOwn skills for Hermes discovery. | 0 | 4 | 100.0% |
| [`modules.lazy_skills`](modules/modules.lazy_skills.py.md) | Skill context injection for planner/worker prompts. | 0 | 4 | 100.0% |
| [`modules.lazy_summarizer`](modules/modules.lazy_summarizer.py.md) | Bounded chain summarizer for the Lazy autonomous loop. | 0 | 2 | 100.0% |
| [`modules/lazyatack.sh`](modules/modules.lazyatack.sh.md) | Nombre del script: lazyatack.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Descripción: Este... | 0 | 30 | 100.0% |
| [`modules/lazybrutesshuserenum.sh`](modules/modules.lazybrutesshuserenum.sh.md) | Función para manejar el interruptor de señal Ctrl+C | 0 | 0 | 100.0% |
| [`modules/lazyclonewars.sh`](modules/modules.lazyclonewars.sh.md) | Lista de repositorios (nombre y URL) | 0 | 0 | 100.0% |
| [`modules.lazycloud`](modules/modules.lazycloud.py.md) | Cloud-native attack module for AWS, Azure, and GCP. | 6 | 16 | 78.3% |
| [`modules/lazycurl.sh`](modules/modules.lazycurl.sh.md) | Nombre del script: lazycurl.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Descripción: Este... | 0 | 3 | 75.0% |
| [`modules.lazyencoder_decoder`](modules/modules.lazyencoder_decoder.py.md) |  | 0 | 10 | 0.0% |
| [`modules/lazyevilwimrm.sh`](modules/modules.lazyevilwimrm.sh.md) |  | 0 | 1 | 50.0% |
| [`modules/lazygat.sh`](modules/modules.lazygat.sh.md) | Nombre del script: lazygath.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Descripción: Este... | 0 | 0 | 100.0% |
| [`modules.lazyk8s`](modules/modules.lazyk8s.py.md) | Container and Kubernetes attack module. | 6 | 23 | 93.3% |
| [`modules/lazylynis.sh`](modules/modules.lazylynis.sh.md) | Verificar si se proporcionó un argumento para el host remoto | 0 | 1 | 100.0% |
| [`modules/lazymasscan.sh`](modules/modules.lazymasscan.sh.md) | Nombre del script: lazymasscan.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Descripción: Este... | 0 | 4 | 20.0% |
| [`modules/lazymobilerevshell.sh`](modules/modules.lazymobilerevshell.sh.md) | Verificar si se pasaron los argumentos de IP y puerto | 0 | 0 | 100.0% |
| [`modules/lazynmap.sh`](modules/modules.lazynmap.sh.md) | Nombre del script: lazynmap.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Descripción: Este... | 0 | 8 | 22.2% |
| [`modules.lazyown_bprfuzzer`](modules/modules.lazyown_bprfuzzer.py.md) | main.py | 1 | 12 | 35.7% |
| [`modules.lazyown_bridge`](modules/modules.lazyown_bridge.py.md) | modules/lazyown_bridge.py ========================== Full-coverage structured catalog of all LazyOwn do_ commands mapped to attack phases, MITRE ATT&CK... | 9 | 33 | 34.9% |
| [`modules.lazyown_metaextract0r`](modules/modules.lazyown_metaextract0r.py.md) | main.py | 0 | 9 | 20.0% |
| [`modules.lazyown_parquet_tool`](modules/modules.lazyown_parquet_tool.py.md) | main.py | 0 | 4 | 100.0% |
| [`modules.lazyownclient`](modules/modules.lazyownclient.py.md) | main.py | 0 | 6 | 14.3% |
| [`modules.lazyownerweb`](modules/modules.lazyownerweb.py.md) |  | 0 | 3 | 0.0% |
| [`modules.lazyownserver`](modules/modules.lazyownserver.py.md) | main.py | 0 | 6 | 14.3% |
| [`modules/lazypsexec.sh`](modules/modules.lazypsexec.sh.md) |  | 0 | 1 | 50.0% |
| [`modules/lazyreverse_shell.sh`](modules/modules.lazyreverse_shell.sh.md) | Nombre del script: lazyreverse_shell.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Descripción... | 0 | 2 | 100.0% |
| [`modules/lazyrtpflood.sh`](modules/modules.lazyrtpflood.sh.md) |  | 0 | 0 | 0.0% |
| [`modules/lazyvpnshield.sh`](modules/modules.lazyvpnshield.sh.md) | Author: Nisrin Ahmed aka Wh1teDrvg0n Modify: grisun0 | 0 | 7 | 12.5% |
| [`modules/lazywps.sh`](modules/modules.lazywps.sh.md) |  | 0 | 1 | 0.0% |
| [`modules.lesson_ingestor`](modules/modules.lesson_ingestor.py.md) | Lesson ingestion bridge between EpisodeReflectionEngine and MoERouter. | 2 | 5 | 75.0% |
| [`modules.lilsplunky`](modules/modules.lilsplunky.py.md) | log_monitor_bot_v2_monolithic.py | 1 | 13 | 86.7% |
| [`modules.linux_advanced_payloads`](modules/modules.linux_advanced_payloads.py.md) | Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants. | 2 | 14 | 82.4% |
| [`modules.listener_manager`](modules/modules.listener_manager.py.md) | Multi-listener manager for LazyOwn C2. | 2 | 12 | 80.0% |
| [`modules.live_surface`](modules/modules.live_surface.py.md) | Live attack-surface graph derived from the world model. | 0 | 1 | 100.0% |
| [`modules.llm_adapter`](modules/modules.llm_adapter.py.md) | LLM adapter facade — single import point for all LLM backends used by lazyc2. | 0 | 10 | 100.0% |
| [`modules.llm_client`](modules/modules.llm_client.py.md) | LazyOwn Unified LLM Client ============================ Single interface for all LLM providers used in LazyOwn: - Groq (cloud, fast inference) - Ollama (local... | 1 | 8 | 100.0% |
| [`modules.llm_evaluator`](modules/modules.llm_evaluator.py.md) | llm_evaluator.py — Records LLM decisions and their outcomes, computes quality metrics, and exports fine-tuning datasets for the LazyOwn auto_loop. | 5 | 18 | 4.2% |
| [`modules.llm_factory`](modules/modules.llm_factory.py.md) | LLM backend factory and selection utilities. | 2 | 12 | 100.0% |
| [`modules.llm_pool`](modules/modules.llm_pool.py.md) | Ordered LLM failover pool with health-aware skipping. | 5 | 9 | 100.0% |
| [`modules.llm_prompts`](modules/modules.llm_prompts.py.md) | Canonical prompt-template and knowledge-base contract for LLM consumers. | 2 | 17 | 100.0% |
| [`modules.log_tamper`](modules/modules.log_tamper.py.md) | Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log. | 2 | 7 | 90.0% |
| [`modules.logging_config`](modules/modules.logging_config.py.md) | Centralized logging configuration for the LazyOwn framework. | 4 | 15 | 85.0% |
| [`modules.loop_ai_bridge`](modules/modules.loop_ai_bridge.py.md) | Single edge between the autonomous loop and the LazyOwn AI stack. | 0 | 11 | 100.0% |
| [`modules.loop_progress`](modules/modules.loop_progress.py.md) | Rich Live milestone panel for the autonomous loop. | 2 | 9 | 100.0% |
| [`modules.macos_payloads`](modules/modules.macos_payloads.py.md) | macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC. | 2 | 11 | 92.9% |
| [`modules.mario`](modules/modules.mario.py.md) |  | 0 | 1 | 0.0% |
| [`modules.mcp_agent_bridge`](modules/modules.mcp_agent_bridge.py.md) | LazyOwn MCP Agent Bridge ======================== Allows Claude (via MCP) to delegate tasks to internal AI agents (Groq / Ollama) running inside LazyOwn... | 3 | 10 | 42.9% |
| [`modules.memory_cleaner`](modules/modules.memory_cleaner.py.md) | Memory artifact cleanup — process memory wipe, environment variable scrub, clipboard clear. | 2 | 5 | 87.5% |
| [`modules.memory_store`](modules/modules.memory_store.py.md) | memory_store.py — Episodic memory for the LazyOwn auto_loop. | 4 | 24 | 3.4% |
| [`modules.metrics`](modules/modules.metrics.py.md) | LazyOwn metrics surface. | 5 | 16 | 100.0% |
| [`modules.mfa_bypass`](modules/modules.mfa_bypass.py.md) | MFA Bypass Toolkit — techniques for circumventing multi-factor authentication. | 3 | 7 | 81.8% |
| [`modules/mkcloudflaretunnel.sh`](modules/modules.mkcloudflaretunnel.sh.md) | cloudflare_tunnel.sh - Download cloudflared and create a tunnel to localhost on a specified port. | 0 | 0 | 100.0% |
| [`modules.module_registry`](modules/modules.module_registry.py.md) | Unified module registry for LazyOwn — catalog, search, use/run workflow. | 2 | 13 | 87.5% |
| [`modules.moe_router`](modules/modules.moe_router.py.md) | modules/moe_router.py ====================== Mixture-of-Experts (MoE) Router for LazyOwn. | 7 | 22 | 65.5% |
| [`modules.morse`](modules/modules.morse.py.md) | Morse code conversion service with interactive driver. | 1 | 6 | 100.0% |
| [`modules/mysql_hookandroot_lib.c`](modules/modules.mysql_hookandroot_lib.c.md) |  | 0 | 6 | 28.6% |
| [`modules.network_opsec`](modules/modules.network_opsec.py.md) | Network OPSEC — proxy chain enforcement, canary detection, traffic randomization. | 2 | 9 | 83.3% |
| [`modules.nmap2csv`](modules/modules.nmap2csv.py.md) | This file is part of nmaptocsv. | 2 | 42 | 26.7% |
| [`modules.notify`](modules/modules.notify.py.md) | Stateless multi-channel notifier for finding events. | 4 | 10 | 100.0% |
| [`modules.nuclei_templates_sync`](modules/modules.nuclei_templates_sync.py.md) | Sync community Nuclei template collections into the LazyOwn marketplace. | 0 | 15 | 100.0% |
| [`modules.obs_parser`](modules/modules.obs_parser.py.md) | modules/obs_parser.py ====================== Observation parser: extracts structured findings from raw tool output. | 5 | 8 | 57.1% |
| [`modules.ooficesod0woodo`](modules/modules.ooficesod0woodo.py.md) |  | 0 | 0 | 0.0% |
| [`modules.operation`](modules/modules.operation.py.md) | Caldera-style operation lifecycle: create, start, pause, resume, stop, status. | 5 | 18 | 33.3% |
| [`modules.operator_profiles`](modules/modules.operator_profiles.py.md) | Multi-operator profile management for LazyOwn team server. | 2 | 13 | 87.5% |
| [`modules.opsec_scorer`](modules/modules.opsec_scorer.py.md) | OPSEC scoring engine — pre-execution noise assessment and gated scoring. | 7 | 12 | 80.0% |
| [`modules.orchestrator_config`](modules/modules.orchestrator_config.py.md) | Operator configuration for the loop core: pipeline stages and auto verbs. | 0 | 9 | 100.0% |
| [`modules.osint_enrich`](modules/modules.osint_enrich.py.md) | Keyless OSINT enrichment for finding evidence. | 0 | 5 | 100.0% |
| [`modules.payload_factory`](modules/modules.payload_factory.py.md) | Native payload generation framework — stagers, stages, singles, formats. | 7 | 20 | 71.4% |
| [`modules.phishing_orchestrator`](modules/modules.phishing_orchestrator.py.md) | Smart Phishing Campaign Orchestrator. | 4 | 9 | 85.7% |
| [`modules.pipeline_engine`](modules/modules.pipeline_engine.py.md) | modules/pipeline_engine.py — Declarative YAML pipelines for LazyOwn ==================================================================== | 19 | 36 | 73.2% |
| [`modules.planner`](modules/modules.planner.py.md) | Fact-based planner — decides the next ability to run. | 6 | 15 | 90.9% |
| [`modules.playbook_engine`](modules/modules.playbook_engine.py.md) | modules/playbook_engine.py =========================== Bridges MITRE ATT&CK (STIX2), Atomic Red Team, WorldModel, and LLMClient into a closed autonomous... | 5 | 11 | 52.9% |
| [`modules.playbook_executor`](modules/modules.playbook_executor.py.md) | Playbook Executor — bridges MITRE ATT&CK playbooks to the pipeline engine. | 7 | 16 | 83.3% |
| [`modules.polymorphic_engine`](modules/modules.polymorphic_engine.py.md) | Polymorphic code generation engine — shellcode mutation and obfuscation. | 3 | 6 | 90.0% |
| [`modules.privesc_predictor`](modules/modules.privesc_predictor.py.md) | Crystal Ball — privilege escalation vector prediction engine. | 2 | 10 | 100.0% |
| [`modules.professional_report`](modules/modules.professional_report.py.md) | Professional Red Team Report Generator. | 3 | 7 | 90.9% |
| [`modules/r.sh`](modules/modules.r.sh.md) | Obtener la versión del kernel actual | 0 | 1 | 100.0% |
| [`modules.reactive_engine`](modules/modules.reactive_engine.py.md) | modules/reactive_engine.py =========================== Parses command output and produces concrete next-action recommendations: - PrivEsc advice (GTFOBins /... | 16 | 21 | 57.9% |
| [`modules.recommender`](modules/modules.recommender.py.md) | LazyOwn Smart Command Recommender =================================== Reads the current session state and asks Groq to rank the best 3-5 next LazyOwn commands... | 0 | 2 | 100.0% |
| [`modules.redteam_gym`](modules/modules.redteam_gym.py.md) | Red Team Gym — gamified pentest training mode. | 0 | 6 | 100.0% |
| [`modules.reflective_dll`](modules/modules.reflective_dll.py.md) | Reflective DLL loading — load PE from memory without touching disk. | 7 | 18 | 84.6% |
| [`modules.resource_script`](modules/modules.resource_script.py.md) | Enhanced resource script engine — variables, conditionals, loops, macros. | 3 | 8 | 75.0% |
| [`modules/reverse-shell.c`](modules/modules.reverse-shell.c.md) |  | 0 | 0 | 0.0% |
| [`modules/revshell.c`](modules/modules.revshell.c.md) |  | 0 | 2 | 0.0% |
| [`modules.rich_tui`](modules/modules.rich_tui.py.md) | Rich-based live TUI dashboard for LazyOwn campaign monitoring. | 1 | 3 | 100.0% |
| [`modules.rl_trainer`](modules/modules.rl_trainer.py.md) | modules/rl_trainer.py ====================== Reinforcement Learning trainer for expert routing in LazyOwn's MoE system. | 6 | 20 | 70.4% |
| [`modules.saas_attacks`](modules/modules.saas_attacks.py.md) | SaaS attacks — Microsoft 365, Google Workspace, Salesforce, ServiceNow exploitation. | 3 | 12 | 62.5% |
| [`modules.search`](modules/modules.search.py.md) | main.py | 0 | 0 | 100.0% |
| [`modules.security_sanitizers`](modules/modules.security_sanitizers.py.md) | Security sanitizers shared across the LazyOwn framework. | 6 | 15 | 100.0% |
| [`modules.selfupdate`](modules/modules.selfupdate.py.md) | Guarded self-update for the LazyOwn working tree. | 2 | 8 | 100.0% |
| [`modules.session_cleanup`](modules/modules.session_cleanup.py.md) | Ephemeral infrastructure cleanup on shell exit. | 0 | 3 | 100.0% |
| [`modules.session_rag`](modules/modules.session_rag.py.md) | session_rag.py — ChromaDB-backed RAG over sessions/ artefacts. | 1 | 8 | 70.0% |
| [`modules.session_reader`](modules/modules.session_reader.py.md) | modules/session_reader.py ========================== Reads LazyOwn C2 session artefacts: - sessions/{client_id}.log (implant CSV: os, pid, hostname, ips, user... | 10 | 19 | 33.3% |
| [`modules.session_state`](modules/modules.session_state.py.md) | LazyOwn Session State ===================== Aggregates live session data from multiple sources into a single sessions/session_state.json snapshot consumed by... | 0 | 3 | 100.0% |
| [`modules.sidequestion`](modules/modules.sidequestion.py.md) | Isolated side-question answering against immutable snapshots. | 4 | 5 | 100.0% |
| [`modules.sleep_obfuscation`](modules/modules.sleep_obfuscation.py.md) | Sleep obfuscation engine for beacon memory evasion. | 7 | 20 | 92.9% |
| [`modules/smbver.sh`](modules/modules.smbver.sh.md) | Author: rewardone Description: Requires root or enough permissions to use tcpdump Will listen for the first 7 packets of a null login and grab the SMB Version... | 0 | 0 | 100.0% |
| [`modules.socks_proxy`](modules/modules.socks_proxy.py.md) | SOCKS5 proxy engine for tunneling traffic through LazyOwn beacons. | 8 | 21 | 96.7% |
| [`modules.staged_delivery`](modules/modules.staged_delivery.py.md) | Staged payload delivery — HTA, Office macros, LNK files, ISO/VHD packaging. | 2 | 9 | 91.7% |
| [`modules.state_manager`](modules/modules.state_manager.py.md) | UnifiedStateManager — single source of truth for all LazyOwn campaign state. | 3 | 30 | 11.8% |
| [`modules.sudo_tiocsti`](modules/modules.sudo_tiocsti.py.md) | tiocsti_advanced.py – Production‑grade TIOCSTI injection with multiple attack modes. | 0 | 9 | 90.0% |
| [`modules.surface_ops`](modules/modules.surface_ops.py.md) | Pure attack-surface helpers (no cmd2): discovery targets, confirm parsing. | 0 | 4 | 100.0% |
| [`modules.tel`](modules/modules.tel.py.md) |  | 0 | 6 | 57.1% |
| [`modules.threat_model`](modules/modules.threat_model.py.md) | threat_model.py — Blue team threat model builder for LazyOwn. | 1 | 3 | 40.0% |
| [`modules.timeline_narrator`](modules/modules.timeline_narrator.py.md) | LazyOwn Timeline Narrator ========================== Reads events.jsonl, groups them into time windows, and asks Groq to generate a concise red-team prose... | 0 | 2 | 100.0% |
| [`modules.timestomper`](modules/modules.timestomper.py.md) | Filesystem timestomping — MACB timestamp manipulation for stealth. | 3 | 8 | 91.7% |
| [`modules/tmp.sh`](modules/modules.tmp.sh.md) |  | 0 | 0 | 0.0% |
| [`modules.toolset`](modules/modules.toolset.py.md) | Typed tool sets per agent role with shell allowlists. | 1 | 4 | 100.0% |
| [`modules.toposwarm_bridge`](modules/modules.toposwarm_bridge.py.md) | modules/toposwarm_bridge.py ============================ Local brain bridge: connects LazyOwn to the TopoSwarm router when cloud LLMs (Groq / Ollama / Claude... | 3 | 14 | 72.2% |
| [`modules.traffic_morpher`](modules/modules.traffic_morpher.py.md) | C2 traffic obfuscation: domain fronting, protocol mimicking, and traffic shaping. | 1 | 10 | 91.7% |
| [`modules.traffic_recorder`](modules/modules.traffic_recorder.py.md) | HTTP traffic recorder with file-tree storage and SQLite index. | 3 | 15 | 100.0% |
| [`modules.ttp_coverage`](modules/modules.ttp_coverage.py.md) | TTP coverage matrix — real-time MITRE ATT&CK technique tracking. | 2 | 8 | 54.5% |
| [`modules.unified_bridge`](modules/modules.unified_bridge.py.md) | UnifiedBridge — single API over all LazyOwn bridges and routing engines. | 7 | 16 | 37.5% |
| [`modules.unified_dashboard`](modules/modules.unified_dashboard.py.md) | Unified campaign dashboard — combines all state sources into one view. | 1 | 5 | 85.7% |
| [`modules/update_db.sh`](modules/modules.update_db.sh.md) | Nombre del script: update_db.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Descripción: Este... | 0 | 0 | 100.0% |
| [`modules.venator`](modules/modules.venator.py.md) |  | 0 | 33 | 0.0% |
| [`modules.vuln_bot_cli`](modules/modules.vuln_bot_cli.py.md) | main.py | 0 | 2 | 33.3% |
| [`modules.vulnbot`](modules/modules.vulnbot.py.md) | vulnbot.py | 1 | 10 | 8.3% |
| [`modules.websocket_beacon`](modules/modules.websocket_beacon.py.md) | WebSocket beacon transport for modern C2 channels. | 2 | 13 | 100.0% |
| [`modules/wineconfig.sh`](modules/modules.wineconfig.sh.md) |  | 0 | 0 | 0.0% |
| [`modules.workspace`](modules/modules.workspace.py.md) | Confined workspace file browser for operators and loop agents. | 0 | 7 | 100.0% |
| [`modules.world_model`](modules/modules.world_model.py.md) | modules/world_model.py ======================= Unified engagement world model for LazyOwn autonomous operations. | 11 | 44 | 55.4% |
| [`modules.yaml_generator`](modules/modules.yaml_generator.py.md) | yaml_generator.py | 1 | 6 | 62.5% |
| [`modules.yara_scanner`](modules/modules.yara_scanner.py.md) | YARA integration for malware classification and IOC scanning. | 1 | 10 | 100.0% |

### `modules/backdoor`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`modules/backdoor/backdoor.c`](modules/modules.backdoor.backdoor.c.md) |  | 0 | 5 | 0.0% |
| [`modules/backdoor/keylogger.h`](modules/modules.backdoor.keylogger.h.md) |  | 0 | 1 | 0.0% |
| [`modules/backdoor/server.c`](modules/modules.backdoor.server.c.md) |  | 0 | 1 | 0.0% |

### `modules/cgi-bin`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`modules.cgi-bin.lazywebshell`](modules/modules.cgi-bin.lazywebshell.py.md) |  | 0 | 0 | 0.0% |
| [`modules/cgi-bin/lazywebshell.sh`](modules/modules.cgi-bin.lazywebshell.sh.md) |  | 0 | 0 | 0.0% |

### `modules/integrations`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`modules.integrations`](modules/modules.integrations.__init__.py.md) | LazyOwn integrations — bridges to external platforms and tools. | 0 | 0 | 100.0% |
| [`modules.integrations.misp_export`](modules/modules.integrations.misp_export.py.md) | modules/integrations/misp_export.py ===================================== Exports LazyOwn session findings as MISP-compatible events (JSON format). | 10 | 13 | 100.0% |
| [`modules.integrations.nuclei_bridge`](modules/modules.integrations.nuclei_bridge.py.md) | modules/integrations/nuclei_bridge.py ======================================= Selects and runs Nuclei templates based on discovered services and CVEs from... | 5 | 11 | 82.4% |
| [`modules.integrations.nuclei_parser`](modules/modules.integrations.nuclei_parser.py.md) | Nuclei JSON output parser — feeds scan results into DB, WorldModel, and recommender. | 2 | 10 | 69.2% |
| [`modules.integrations.searchsploit`](modules/modules.integrations.searchsploit.py.md) | modules/integrations/searchsploit.py ====================================== Bridges searchsploit CLI and ExploitDB with LazyOwn CVE/finding data. | 5 | 15 | 85.7% |

### `modules/legacy`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`modules.legacy`](modules/modules.legacy.__init__.py.md) | Backward-compatibility shims for deprecated scripts. | 0 | 0 | 100.0% |

### `modules/rootkit`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`modules/rootkit/mr.c`](modules/modules.rootkit.mr.c.md) |  | 2 | 31 | 0.0% |
| [`modules/rootkit/mrhyde.c`](modules/modules.rootkit.mrhyde.c.md) |  | 2 | 36 | 2.6% |
| [`modules/rootkit/mrhyde2.c`](modules/modules.rootkit.mrhyde2.c.md) |  | 2 | 33 | 2.8% |
| [`modules/rootkit/mrhyde3.c`](modules/modules.rootkit.mrhyde3.c.md) |  | 5 | 41 | 10.6% |
| [`modules/rootkit/rootkit.asm`](modules/modules.rootkit.rootkit.asm.md) |  | 0 | 1 | 0.0% |
| [`modules/rootkit/rootkit.c`](modules/modules.rootkit.rootkit.c.md) |  | 0 | 6 | 14.3% |

### `modules/scripts`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`modules/scripts/clean_history.sh.sh`](modules/modules.scripts.clean_history.sh.sh.md) |  | 0 | 0 | 0.0% |

### `modules/tools`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`modules.tools`](modules/modules.tools.__init__.py.md) | Reusable development tools for the LazyOwn autonomous loop. | 0 | 0 | 100.0% |
| [`modules.tools.loop_smoke`](modules/modules.tools.loop_smoke.py.md) | End-to-end smoke of the shared loop runner (no LLM, no network). | 2 | 8 | 100.0% |
| [`modules.tools.monitor_smoke`](modules/modules.tools.monitor_smoke.py.md) | Headless smoke of the Textual worker monitor (``lazy_view``). | 0 | 2 | 100.0% |

### `modules/win_rootkit`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`modules/win_rootkit/backup.c`](modules/modules.win_rootkit.backup.c.md) |  | 2 | 15 | 0.0% |
| [`modules/win_rootkit/mrhyde.c`](modules/modules.win_rootkit.mrhyde.c.md) |  | 0 | 18 | 36.8% |
| [`modules/win_rootkit/win_rin3_rootkit.cs`](modules/modules.win_rootkit.win_rin3_rootkit.cs.md) |  | 6 | 4 | 0.0% |
| [`modules/win_rootkit/win_ring3_rootkit.c`](modules/modules.win_rootkit.win_ring3_rootkit.c.md) |  | 3 | 24 | 10.7% |
| [`modules/win_rootkit/win_ring3_rootkit.cpp`](modules/modules.win_rootkit.win_ring3_rootkit.cpp.md) |  | 0 | 9 | 0.0% |

### `plugins`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`plugins/generate_c_reverse_shell.lua`](modules/plugins.generate_c_reverse_shell.lua.md) |  | 0 | 2 | 33.3% |
| [`plugins/generate_cleanup_commands.lua`](modules/plugins.generate_cleanup_commands.lua.md) |  | 0 | 1 | 50.0% |
| [`plugins/generate_html_payload.lua`](modules/plugins.generate_html_payload.lua.md) |  | 0 | 1 | 0.0% |
| [`plugins/generate_lateral_command.lua`](modules/plugins.generate_lateral_command.lua.md) |  | 0 | 1 | 50.0% |
| [`plugins/generate_linux_asm_reverse_shell.lua`](modules/plugins.generate_linux_asm_reverse_shell.lua.md) |  | 0 | 2 | 33.3% |
| [`plugins/generate_linux_raw_shellcode.lua`](modules/plugins.generate_linux_raw_shellcode.lua.md) |  | 0 | 1 | 0.0% |
| [`plugins/generate_lolbird.lua`](modules/plugins.generate_lolbird.lua.md) |  | 0 | 6 | 42.9% |
| [`plugins/generate_msfvenom_loader.lua`](modules/plugins.generate_msfvenom_loader.lua.md) |  | 0 | 5 | 83.3% |
| [`plugins/generate_msfvenom_loader_windows.lua`](modules/plugins.generate_msfvenom_loader_windows.lua.md) |  | 0 | 1 | 50.0% |
| [`plugins/generate_reverse_shell.lua`](modules/plugins.generate_reverse_shell.lua.md) |  | 0 | 1 | 0.0% |
| [`plugins/generate_stub.lua`](modules/plugins.generate_stub.lua.md) |  | 0 | 5 | 50.0% |
| [`plugins/init_plugins.lua`](modules/plugins.init_plugins.lua.md) |  | 0 | 1 | 50.0% |
| [`plugins/kerberos_harvest.lua`](modules/plugins.kerberos_harvest.lua.md) |  | 0 | 1 | 0.0% |
| [`plugins/lolbas_bitsadmin_exe.lua`](modules/plugins.lolbas_bitsadmin_exe.lua.md) |  | 0 | 0 | 0.0% |
| [`plugins/lolbas_certutil_download_exec.lua`](modules/plugins.lolbas_certutil_download_exec.lua.md) |  | 0 | 3 | 0.0% |
| [`plugins/lolbas_certutil_exe.lua`](modules/plugins.lolbas_certutil_exe.lua.md) |  | 0 | 1 | 50.0% |
| [`plugins/lolbas_mshta_js.lua`](modules/plugins.lolbas_mshta_js.lua.md) |  | 0 | 0 | 0.0% |
| [`plugins/lolbas_mshta_reverse_shell.lua`](modules/plugins.lolbas_mshta_reverse_shell.lua.md) |  | 0 | 0 | 0.0% |
| [`plugins/lolbas_rundll32_dll.lua`](modules/plugins.lolbas_rundll32_dll.lua.md) |  | 0 | 0 | 0.0% |
| [`plugins/lolbas_wmic_xsl_execution.lua`](modules/plugins.lolbas_wmic_xsl_execution.lua.md) |  | 0 | 1 | 0.0% |
| [`plugins/parse_nmap_with_xmlstarlet.lua`](modules/plugins.parse_nmap_with_xmlstarlet.lua.md) |  | 0 | 1 | 0.0% |
| [`plugins/run_nuclei_on_nmap_files.lua`](modules/plugins.run_nuclei_on_nmap_files.lua.md) |  | 0 | 1 | 0.0% |
| [`plugins/run_python_rev_c2.lua`](modules/plugins.run_python_rev_c2.lua.md) |  | 0 | 1 | 50.0% |
| [`plugins/rundll32_sct_from_url.lua`](modules/plugins.rundll32_sct_from_url.lua.md) |  | 0 | 4 | 40.0% |
| [`plugins/validate_shellcode.lua`](modules/plugins.validate_shellcode.lua.md) |  | 0 | 4 | 80.0% |
| [`plugins/visualize_network.lua`](modules/plugins.visualize_network.lua.md) |  | 0 | 1 | 0.0% |

### `poc_tui`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`poc_tui.__main__`](modules/poc_tui.__main__.py.md) | Entry point: python3 -m poc_tui | 0 | 0 | 100.0% |
| [`poc_tui.app`](modules/poc_tui.app.py.md) | LazyOwn TUI Shell — Proof of Concept. | 5 | 33 | 48.7% |
| [`poc_tui.config`](modules/poc_tui.config.py.md) | Payload.json configuration manager for the TUI shell. | 1 | 6 | 50.0% |
| [`poc_tui.plugin_loader`](modules/poc_tui.plugin_loader.py.md) | Unified plugin loader — YAML addons, Lua plugins, and .tool files. | 2 | 2 | 80.0% |
| [`poc_tui.run`](modules/poc_tui.run.py.md) | Convenience launcher that symlinks LazyOwn dirs and starts the TUI. | 0 | 1 | 50.0% |

### `scripts`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`scripts`](modules/scripts.__init__.py.md) | Repository-side maintenance scripts. | 0 | 0 | 100.0% |
| [`scripts.activate_migrations`](modules/scripts.activate_migrations.py.md) | Activate dormant CommandSet migrations. | 1 | 6 | 75.0% |
| [`scripts.backfill_addon_os_trigger`](modules/scripts.backfill_addon_os_trigger.py.md) | One-shot backfill: add ``os`` and ``trigger`` keys to every lazyaddon. | 0 | 5 | 100.0% |
| [`scripts.check_contract_manifest`](modules/scripts.check_contract_manifest.py.md) | Verify that documented contracts still exist on disk. | 1 | 3 | 100.0% |
| [`scripts.fix_migrated_classes`](modules/scripts.fix_migrated_classes.py.md) |  | 0 | 0 | 0.0% |
| [`scripts.generate_sbom`](modules/scripts.generate_sbom.py.md) | Generate a minimal CycloneDX SBOM from the pinned requirements files. | 0 | 5 | 100.0% |
| [`scripts.journal`](modules/scripts.journal.py.md) | Read-before-you-write journal over GitHub Discussions. | 3 | 6 | 100.0% |
| [`scripts/lazy_hermes_ask.sh`](modules/scripts.lazy_hermes_ask.sh.md) | lazy_hermes_ask.sh — detached Hermes task runner for LazyOwn. | 0 | 0 | 100.0% |
| [`scripts/lazy_llamacpp_serve.sh`](modules/scripts.lazy_llamacpp_serve.sh.md) | lazy_llamacpp_serve.sh — idempotent llama.cpp server manager for LazyOwn. | 0 | 1 | 50.0% |
| [`scripts/lazy_llamacpp_setup.sh`](modules/scripts.lazy_llamacpp_setup.sh.md) | lazy_llamacpp_setup.sh — one-time local LLM setup for LazyOwn users. | 0 | 1 | 50.0% |
| [`scripts/lazy_msf_lab.sh`](modules/scripts.lazy_msf_lab.sh.md) | lazy_msf_lab.sh — Metasploitable2 smoke lab manager for LazyOwn. | 0 | 0 | 100.0% |
| [`scripts.lazy_opencode_config`](modules/scripts.lazy_opencode_config.py.md) | Patch operator agent configs to use the Lazy llama.cpp server. | 0 | 2 | 100.0% |
| [`scripts.migrate_commandsets`](modules/scripts.migrate_commandsets.py.md) | Merge _migrated.py CommandSet methods into clean phase modules. | 0 | 2 | 66.7% |
| [`scripts.migrate_lazyown`](modules/scripts.migrate_lazyown.py.md) | Staged migration script: extract do_* methods from lazyown.py into cli/commands/. | 0 | 4 | 80.0% |
| [`scripts/mutate.sh`](modules/scripts.mutate.sh.md) | Mutation gate for LazyOwn. | 0 | 3 | 25.0% |
| [`scripts.patch_playbook_atomic_ids`](modules/scripts.patch_playbook_atomic_ids.py.md) | Patch APT playbooks: replace placeholder atomic_ids with real technique_ids. | 0 | 0 | 100.0% |
| [`scripts/publish_wiki.sh`](modules/scripts.publish_wiki.sh.md) | Publish LazyOwn documentation to the GitHub wiki. | 0 | 8 | 11.1% |
| [`scripts.read_journal`](modules/scripts.read_journal.py.md) | Print the recent engineering journal before a change is written. | 0 | 1 | 100.0% |
| [`scripts/setup_hermes_mcp.sh`](modules/scripts.setup_hermes_mcp.sh.md) | setup_hermes_mcp.sh — register LazyOwn MCP server in Hermes Agent config Usage: bash scripts/setup_hermes_mcp.sh [--check] --check verify registration without... | 0 | 0 | 100.0% |
| [`scripts/smoke_onboarding.sh`](modules/scripts.smoke_onboarding.sh.md) | Smoke test for the 5-minute onboarding path. | 0 | 1 | 50.0% |
| [`scripts.sync_doc_stats`](modules/scripts.sync_doc_stats.py.md) | Sync documentation numbers with the live codebase — single source of truth. | 0 | 6 | 100.0% |
| [`scripts.top_tier_check`](modules/scripts.top_tier_check.py.md) | Top-tier hygiene audit for LazyOwn. | 0 | 10 | 9.1% |
| [`scripts.update_apt_atomic_ids`](modules/scripts.update_apt_atomic_ids.py.md) | Update APT playbooks with real Atomic Red Team test IDs. | 0 | 2 | 66.7% |
| [`scripts/validate_agent_contract.sh`](modules/scripts.validate_agent_contract.sh.md) | validate_agent_contract.sh CI validation of the AGENTS.md branching model and coding standards. | 0 | 5 | 50.0% |

### `scripts/devtools`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`scripts.devtools.command_audit`](modules/scripts.devtools.command_audit.py.md) | Audit every registered shell command for dispatch and parser errors. | 1 | 3 | 100.0% |
| [`scripts.devtools.core_smoke`](modules/scripts.devtools.core_smoke.py.md) | Smoke check for the public surfaces documented in CORE.md. | 1 | 3 | 100.0% |

### `skills`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`skills.aci_planner`](modules/skills.aci_planner.py.md) | Autonomous Campaign Intelligence (ACI) Planner =============================================== Decomposes a natural-language engagement goal into a MITRE... | 6 | 19 | 100.0% |
| [`skills.autonomous_daemon`](modules/skills.autonomous_daemon.py.md) | skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon ================================================================== Bridges LazyOwn... | 26 | 63 | 87.8% |
| [`skills.autonomous_replay`](modules/skills.autonomous_replay.py.md) | Deterministic replay of past autonomous-daemon runs. | 5 | 9 | 100.0% |
| [`skills.daemon_control`](modules/skills.daemon_control.py.md) | Operator steering layer for the LazyOwn autonomous daemon. | 3 | 23 | 100.0% |
| [`skills.daemon_health`](modules/skills.daemon_health.py.md) | Daemon health monitor — watchdog for the autonomous daemon and C2 listeners. | 1 | 12 | 83.3% |
| [`skills.heartbeat`](modules/skills.heartbeat.py.md) | LazyOwn Heartbeat ================= Lightweight background process that drives the event engine. | 0 | 5 | 33.3% |
| [`skills.hive_mind`](modules/skills.hive_mind.py.md) | skills/hive_mind.py — LazyOwn Borg Hive Mind ============================================== Multi-agent cognitive architecture where Claude (MCP) is the... | 18 | 72 | 89.0% |
| [`skills.lazyown_automapper`](modules/skills.lazyown_automapper.py.md) | LazyOwn MCP Auto-Mapper ======================== Discovers LazyOwn extensions at startup and returns MCP Tool definitions + a runtime dispatch table. | 1 | 7 | 77.8% |
| [`skills.lazyown_campaign`](modules/skills.lazyown_campaign.py.md) | LazyOwn CampaignStore ===================== Groups multiple targets under a single named penetration-test engagement. | 4 | 17 | 86.4% |
| [`skills.lazyown_claudemd`](modules/skills.lazyown_claudemd.py.md) | LazyOwn CLAUDE.md Hierarchical Loader (Claude Code style) | 1 | 7 | 77.8% |
| [`skills.lazyown_context`](modules/skills.lazyown_context.py.md) | LazyOwn Context Compaction Pipeline — 5-layer graduated compression (Claude Code style) | 2 | 9 | 75.0% |
| [`skills.lazyown_daemon`](modules/skills.lazyown_daemon.py.md) | LazyOwn Unified Daemon ====================== Replaces three separate background processes with a single asyncio daemon: | 0 | 9 | 100.0% |
| [`skills.lazyown_facts`](modules/skills.lazyown_facts.py.md) | LazyOwn FactStore ================= Structured fact extraction from nmap XML files and pwntomate tool output. | 23 | 45 | 50.7% |
| [`skills.lazyown_groq_agents`](modules/skills.lazyown_groq_agents.py.md) | skills/lazyown_groq_agents.py ============================== Translates LazyOwn MCP tools into Groq-native tool-calling format and provides a multi-agent pool... | 1 | 11 | 30.8% |
| [`skills.lazyown_hooks`](modules/skills.lazyown_hooks.py.md) | LazyOwn Hook Pipeline (Claude Code style) | 2 | 11 | 71.4% |
| [`skills.lazyown_llm`](modules/skills.lazyown_llm.py.md) | LazyOwn LLM Bridge — MCP Edition ================================= Unified satellite-model interface for lazyown_mcp.py. | 2 | 7 | 50.0% |
| [`skills.lazyown_mcp`](modules/skills.lazyown_mcp.py.md) | LazyOwn MCP Server Exposes LazyOwn framework capabilities as MCP tools for Claude Code and Claude web. | 0 | 5 | 50.0% |
| [`skills.lazyown_mcp_helpers`](modules/skills.lazyown_mcp_helpers.py.md) | LazyOwn MCP helper functions — pure logic, no MCP server imports. | 3 | 16 | 85.0% |
| [`skills.lazyown_mcp_opencode`](modules/skills.lazyown_mcp_opencode.py.md) | LazyOwn MCP OpenCode bridge. | 0 | 3 | 75.0% |
| [`skills.lazyown_objective`](modules/skills.lazyown_objective.py.md) | LazyOwn Objective Store ======================= Priority-queue for high-level attack objectives. | 3 | 25 | 41.4% |
| [`skills.lazyown_parquet_db`](modules/skills.lazyown_parquet_db.py.md) | LazyOwn Parquet Knowledge Base ================================ Centralises session history and contextual knowledge in the parquets/ directory. | 1 | 15 | 70.6% |
| [`skills.lazyown_permissions`](modules/skills.lazyown_permissions.py.md) | LazyOwn Permission System — Deny-First Rule Evaluation (Claude Code style) | 3 | 9 | 30.8% |
| [`skills.lazyown_policy`](modules/skills.lazyown_policy.py.md) | LazyOwn Policy Engine ===================== Four-tier cascading outcome classifier with reward-based transition learning. | 35 | 66 | 81.4% |
| [`skills.lazyown_session`](modules/skills.lazyown_session.py.md) | LazyOwn Append-Only Session Transcripts (Claude Code style) | 1 | 11 | 69.2% |
| [`skills.mcp_generated_tools`](modules/skills.mcp_generated_tools.py.md) | Auto-generated MCP tool handlers from command_index.json. | 0 | 2 | 100.0% |
| [`skills.mcp_lazy`](modules/skills.mcp_lazy.py.md) | Single helper behind every lazy optional import of the MCP server. | 0 | 1 | 100.0% |
| [`skills/mcp_restart.sh`](modules/skills.mcp_restart.sh.md) | LazyOwn MCP restart helper Kills ALL lazyown_mcp instances (stdio + SSE) and relaunches the SSE daemon. | 0 | 0 | 100.0% |
| [`skills.mcp_tool_generator`](modules/skills.mcp_tool_generator.py.md) | Auto-generate MCP tool handlers from cli/command_index.json. | 0 | 8 | 77.8% |
| [`skills.sessions_watcher`](modules/skills.sessions_watcher.py.md) | LazyOwn Sessions Watcher ======================== Watchdog daemon over sessions/. | 0 | 1 | 50.0% |
| [`skills/setup.sh`](modules/skills.setup.sh.md) | ============================================================================= LazyOwn MCP — One-time system setup Configures sudoers NOPASSWD and Linux... | 0 | 5 | 33.3% |
| [`skills.swan_agent`](modules/skills.swan_agent.py.md) | skills/swan_agent.py — LazyOwn SWAN Agent ========================================== Scalable Weighted Adaptive Network agent coordinator. | 9 | 16 | 92.3% |
| [`skills.toposwarm_autonomous`](modules/skills.toposwarm_autonomous.py.md) | skills/toposwarm_autonomous.py ================================ TopoSwarm Autonomous Red Team Agent ==================================== Drives LazyOwn through... | 2 | 6 | 22.2% |
| [`skills.unified_orchestrator`](modules/skills.unified_orchestrator.py.md) | Unified orchestrator facade collapsing daemon, hive and SWAN into one surface. | 12 | 30 | 100.0% |
| [`skills.update_knowledge`](modules/skills.update_knowledge.py.md) | LazyOwn Knowledge Refresh ========================== Refreshes the session_knowledge.parquet from the current CSV and optionally trains the sklearn classifier. | 0 | 1 | 50.0% |

### `skills/claude_md_orchestrator`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`skills.claude_md_orchestrator`](modules/skills.claude_md_orchestrator.__init__.py.md) | Public API for the claude_md_orchestrator skill. | 0 | 0 | 100.0% |
| [`skills.claude_md_orchestrator.bdd_agent`](modules/skills.claude_md_orchestrator.bdd_agent.py.md) | Behavior-Driven Development agent. | 1 | 1 | 100.0% |
| [`skills.claude_md_orchestrator.boy_scout`](modules/skills.claude_md_orchestrator.boy_scout.py.md) | Boy Scout refactor pass. | 1 | 2 | 100.0% |
| [`skills.claude_md_orchestrator.cicd_agent`](modules/skills.claude_md_orchestrator.cicd_agent.py.md) | CI and CD agent. | 1 | 1 | 100.0% |
| [`skills.claude_md_orchestrator.config`](modules/skills.claude_md_orchestrator.config.py.md) | Centralized configuration for the claude_md_orchestrator skill. | 1 | 11 | 100.0% |
| [`skills.claude_md_orchestrator.documentation_agent`](modules/skills.claude_md_orchestrator.documentation_agent.py.md) | Documentation agent. | 1 | 1 | 100.0% |
| [`skills.claude_md_orchestrator.models`](modules/skills.claude_md_orchestrator.models.py.md) | Data models for the claude_md_orchestrator skill. | 10 | 21 | 100.0% |
| [`skills.claude_md_orchestrator.orchestrator`](modules/skills.claude_md_orchestrator.orchestrator.py.md) | Orchestrator that wires the agents into a deterministic pipeline. | 1 | 3 | 100.0% |
| [`skills.claude_md_orchestrator.parser`](modules/skills.claude_md_orchestrator.parser.py.md) | Parser that turns a CLAUDE.md into actionable contracts. | 0 | 2 | 100.0% |
| [`skills.claude_md_orchestrator.reviewer_agent`](modules/skills.claude_md_orchestrator.reviewer_agent.py.md) | Code Reviewer and Quality Assurance agent. | 1 | 2 | 100.0% |
| [`skills.claude_md_orchestrator.sdd_agent`](modules/skills.claude_md_orchestrator.sdd_agent.py.md) | Spec-Driven Development agent. | 1 | 1 | 100.0% |
| [`skills.claude_md_orchestrator.tdd_agent`](modules/skills.claude_md_orchestrator.tdd_agent.py.md) | Test-Driven Development agent. | 1 | 2 | 100.0% |
| [`skills.claude_md_orchestrator.validators`](modules/skills.claude_md_orchestrator.validators.py.md) | DoD validators for every artifact the orchestrator produces. | 1 | 14 | 100.0% |

### `skills/hermes-lazyown`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`skills.hermes-lazyown`](modules/skills.hermes-lazyown.__init__.py.md) | Hermes-LazyOwn integration package. | 0 | 0 | 100.0% |
| [`skills.hermes-lazyown.claudemd_rules`](modules/skills.hermes-lazyown.claudemd_rules.py.md) | Dynamic Claude.md rule generator for the Hermes-LazyOwn integration. | 1 | 8 | 90.0% |
| [`skills.hermes-lazyown.config_bridge`](modules/skills.hermes-lazyown.config_bridge.py.md) | Configuration bridge: unifies LazyOwn payload.json, environment variables, and fallback defaults into a single read-only configuration source. | 2 | 10 | 92.3% |
| [`skills.hermes-lazyown.constants`](modules/skills.hermes-lazyown.constants.py.md) | Central constants for the Hermes-LazyOwn integration layer. | 5 | 10 | 100.0% |
| [`skills.hermes-lazyown.executor`](modules/skills.hermes-lazyown.executor.py.md) | LazyOwn command executor for the Hermes-LazyOwn integration. | 2 | 6 | 77.8% |
| [`skills.hermes-lazyown.hermes_sync`](modules/skills.hermes-lazyown.hermes_sync.py.md) | Hermes-native synchronization layer. | 4 | 10 | 86.7% |
| [`skills.hermes-lazyown.mcp_server`](modules/skills.hermes-lazyown.mcp_server.py.md) | Hermes-native MCP server for LazyOwn. | 0 | 3 | 50.0% |
| [`skills.hermes-lazyown.output_compactor`](modules/skills.hermes-lazyown.output_compactor.py.md) | Phase-aware output compaction for the Hermes-LazyOwn integration. | 8 | 11 | 85.0% |

### `source`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`source.conf`](modules/source.conf.py.md) | Configuration file for the Sphinx documentation builder. | 0 | 0 | 100.0% |

### `static/js`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`static/js/particles.js`](modules/static.js.particles.js.md) | ----------------------------------------------- Author : Vincent Garreau - vincentgarreau.com MIT license: http://opensource.org/licenses/MIT Demo / Generator... | 0 | 11 | 8.3% |
| [`static/js/quill-2.0.3.js`](modules/static.js.quill-2.0.3.js.md) |  | 71 | 21 | 98.9% |
| [`static/js/tippy-6.js`](modules/static.js.tippy-6.js.md) |  | 0 | 3 | 0.0% |
| [`static/js/xterm-addon-fit-0.7.0.js`](modules/static.js.xterm-addon-fit-0.7.0.js.md) |  | 0 | 0 | 0.0% |
| [`static/js/xterm-addon-web-links-0.5.0.js`](modules/static.js.xterm-addon-web-links-0.5.0.js.md) |  | 0 | 4 | 0.0% |
| [`static/js/xterm.js`](modules/static.js.xterm.js.md) |  | 48 | 6 | 0.0% |

### `tools`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`tools.contract_check`](modules/tools.contract_check.py.md) | Contract conformance checker for single-file LAZY port modules. | 0 | 2 | 100.0% |
| [`tools.extract_cluster`](modules/tools.extract_cluster.py.md) | Extract a named cluster of do_* methods from a CommandSet module. | 0 | 4 | 100.0% |
| [`tools.gen_demo_gifs`](modules/tools.gen_demo_gifs.py.md) | Generate LazyOwn demo GIFs without external services. | 0 | 3 | 100.0% |
| [`tools.gen_demo_gifs_extra`](modules/tools.gen_demo_gifs_extra.py.md) | Additional LazyOwn demo GIFs. | 0 | 1 | 100.0% |
