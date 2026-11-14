# Index (page 2 of 4)
Previous: [INDEX.md](INDEX.md)

| File | Purpose | Subsystem | Symbols | Used by |
|------|---------|-----------|---------|---------|
| `modules/gcp_attacks.py` | GCP privilege escalation — service account impersonation, Cloud Functions, GCS enumeration. | modules | 11 | 1 |
| `modules/generate_tools.py` | - | modules | 1 | 0 |
| `modules/goals.py` | Goal decomposition round-0 with constraints and proof. | modules | 13 | 3 |
| `modules/golden_path.py` | Deterministic attack-path solver over the LazyOwn world model. | modules | 15 | 0 |
| `modules/gpo_abuse.py` | GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation. | modules | 16 | 1 |
| `modules/guard_rules.py` | Seeded guard rules that arm the planner filter before any attribution data. | modules | 15 | 3 |
| `modules/guardrails/__init__.py` | Operator-facing guardrail harness: tiers, capacity, checkpoints. | guardrails | 0 | 4 |
| `modules/guardrails/advisories.py` | Non-blocking advisories and feature degradation. | guardrails | 15 | 2 |
| `modules/guardrails/budget.py` | Bounded capacity accounting with strict priority reservation. | guardrails | 16 | 2 |
| `modules/guardrails/checkpoints.py` | Checkpoint ledger with warm-restart recovery. | guardrails | 7 | 2 |
| `modules/guardrails/contracts.py` | Contracts for the execution guardrail harness. | guardrails | 10 | 3 |
| `modules/guardrails/harness.py` | Execution harness facade: guarded runs, warm restart, degradation. | guardrails | 11 | 2 |
| `modules/gui_askpass.sh` | — SUDO_ASKPASS helper for LazyOwn MCP  Used by: sudo -A <script>  (set SUDO_ASKPASS to this... | modules | 5 | 0 |
| `modules/gym_cleanup.py` | Gym machine cleanup on LazyOwn exit. | modules | 2 | 3 |
| `modules/gym_matrix_runner.py` | Ordered Metasploitable 2 gym matrix runner. | modules | 6 | 0 |
| `modules/gym_registry.py` | Gym definitions and persistent run state. | modules | 28 | 5 |
| `modules/gym_winbox_runner.py` | Ordered WinBox gym matrix runner. | modules | 4 | 0 |
| `modules/harness.py` | Deterministic harness gate for the LazyOwn loop. | modules | 2 | 4 |
| `modules/hash_cracker.py` | Hash cracking pipeline — John the Ripper and Hashcat integration. | modules | 17 | 2 |
| `modules/hive_invoke.py` | modules/hive_invoke.py | modules | 7 | 0 |
| `modules/hostdiscover.sh` | - | modules | 2 | 0 |
| `modules/hunt_verify.py` | Evidence verdict verification for hunting and chain stages. | modules | 16 | 3 |
| `modules/ia_code_analysis.py` | CodeAnalyzer: Analyzes source code in a directory and its subdirectories. | modules | 8 | 0 |
| `modules/ia_logs_analysis.py` | Author: Your Name Email: youremail@example.com Creation Date: 10/06/2024 License: AGPL v3... | modules | 7 | 0 |
| `modules/ia_network_analysis.py` | Autor: grisun0 Fecha de creación: 30/01/2025 Licencia: AGPL v3  Descripción: Bot de monitoreo de... | modules | 4 | 0 |
| `modules/img2bin.py` | - | modules | 2 | 0 |
| `modules/integrations/__init__.py` | LazyOwn integrations — bridges to external platforms and tools. | integrations | 0 | 0 |
| `modules/integrations/misp_export.py` | modules/integrations/misp_export.py | integrations | 39 | 2 |
| `modules/integrations/nuclei_bridge.py` | modules/integrations/nuclei_bridge.py | integrations | 29 | 3 |
| `modules/integrations/nuclei_parser.py` | Nuclei JSON output parser — feeds scan results into DB, WorldModel, and recommender. | integrations | 17 | 2 |
| `modules/integrations/searchsploit.py` | modules/integrations/searchsploit.py | integrations | 27 | 1 |
| `modules/intel_fusion.py` | Sessions attack-intel fusion: data -> information -> intelligence. | modules | 35 | 7 |
| `modules/intelligence_engine.py` | IntelligenceEngine — unified collection→analysis→intelligence pipeline. | modules | 33 | 4 |
| `modules/intercept.py` | User-configurable tool-call interception layer with human-in-loop approvals. | modules | 27 | 7 |
| `modules/internal_discover.sh` | - | modules | 0 | 0 |
| `modules/iptables_portforward.sh` | - | modules | 1 | 0 |
| `modules/jsonl_tail.py` | Incremental JSONL reader shared by the monitor TUI and the loop runner. | modules | 3 | 3 |
| `modules/jwtexploit.py` | - | modules | 0 | 0 |
| `modules/k8s_attacks.py` | Kubernetes attack module — RBAC enumeration, pod escape, etcd access, Helm abuse. | modules | 11 | 1 |
| `modules/kerberoasting.py` | Advanced Kerberoasting — targeted SPN enumeration, AES-only attacks, hashcat integration. | modules | 18 | 1 |
| `modules/kerberos_core.py` | Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. | modules | 35 | 2 |
| `modules/kerberos_tickets.py` | Kerberos ticket forgery attacks — silver, golden, diamond, sapphire tickets. | modules | 34 | 1 |
| `modules/kill_chain_viz.py` | SVG / HTML kill-chain visualizer — generates standalone HTML with embedded SVG. | modules | 5 | 1 |
| `modules/killchain.py` | Unified kill-chain — single source of truth consumed by all surfaces. | modules | 25 | 25 |
| `modules/kivi.py` | - | modules | 3 | 0 |
| `modules/lab_runtime.py` | Lab runtime: Docker lifecycle for practice targets and cyber ranges. | modules | 19 | 3 |
| `modules/lazy_agent.py` | Agentic tool-calling bridge for the loop and the main agent. | modules | 32 | 4 |
| `modules/lazy_autofire.py` | Lazy autofire: exploit intelligence closing the loop into chains. | modules | 13 | 1 |
| `modules/lazy_blindspot.py` | Blindspot review contract for the lazy autonomous loop. | modules | 10 | 2 |
| `modules/lazy_bridge.py` | Bidirectional LAZY <-> LazyOwn bridge. | modules | 21 | 7 |
| `modules/lazy_checks.py` | Validation plans as data: re-read observed checks through version math. | modules | 4 | 1 |
| `modules/lazy_cli_bridge.py` | Full CLI catalog for the Lazy autonomous loop. | modules | 15 | 8 |
| `modules/lazy_commander.py` | Fleet commander: allocate the next work slice across loop tasks. | modules | 11 | 2 |
| `modules/lazy_continuation.py` | Task continuation records: campaign memory that survives loop restarts. | modules | 8 | 0 |
| `modules/lazy_creds.py` | Default-credential knowledge base for LazyOwn. | modules | 7 | 0 |
| `modules/lazy_cve_feed.py` | Keyless CVE intelligence feeds and version-aware service correlation. | modules | 26 | 5 |
| `modules/lazy_deviations.py` | Planned-versus-actual deviation ledger for loop and chain runs. | modules | 12 | 4 |
| `modules/lazy_drafts.py` | Injected objective drafts: close the lazy_drafts handoff loop. | modules | 2 | 1 |
| `modules/lazy_engine.py` | Lazy autonomous loop engine: single orchestrator for lazy_* commands. | modules | 1 | 47 |
| `modules/lazy_exposure.py` | Target exposure report for LazyOwn. | modules | 14 | 5 |
| `modules/lazy_fallback.py` | Adaptive fallback alternatives for failed chain techniques. | modules | 9 | 3 |
| `modules/lazy_feedmatch.py` | Exploit feed matching for LazyOwn. | modules | 18 | 6 |
| `modules/lazy_finalizer.py` | Evidence-gated finalization for the autonomous loop and apt_chain. | modules | 3 | 1 |
| `modules/lazy_findings.py` | Engagement findings ledger: state machine plus reproducible evidence. | modules | 27 | 2 |
| `modules/lazy_heat.py` | Heat tiers and version math for CVE correlation. | modules | 15 | 11 |
| `modules/lazy_hostscore.py` | Host heat score: deterministic 0-100 priority for every known host. | modules | 5 | 2 |
| `modules/lazy_installer.py` | Capability installer for the Lazy autonomous loop. | modules | 6 | 3 |
| `modules/lazy_intel.py` | Intel feed from the Lazy autonomous loop. | modules | 14 | 6 |
| `modules/lazy_inventory.py` | Host-reported inventory for LazyOwn. | modules | 7 | 0 |
| `modules/lazy_ledger.py` | Freshness ledger: TTL windows per verb and target for the loop worker. | modules | 11 | 3 |
| `modules/lazy_loop.py` | Lazy autonomous loop for LazyOwn. | modules | 481 | 97 |
| `modules/lazy_match_policy.py` | Match policy doctrine: what may claim a match and what stays a lead. | modules | 14 | 1 |
| `modules/lazy_mentions.py` | LAZY chat mentions with multi-type search and scroll pagination. | modules | 15 | 4 |
| `modules/lazy_netattack.py` | Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay. | modules | 12 | 1 |
| `modules/lazy_objective_queue.py` | Objective queue plumbing: the autonomous loop's read side of the objective store. | modules | 9 | 0 |
| `modules/lazy_oob.py` | Local OOB canary for blind SSRF/RCE detection. | modules | 18 | 0 |
| `modules/lazy_orchestrator_feedback.py` | Organic orchestrator training from loop usage. | modules | 11 | 5 |
| `modules/lazy_osinfer.py` | Target OS inference and OS-aware verb gating. | modules | 11 | 0 |
| `modules/lazy_probes.py` | Read-only validation command registry for LazyOwn. | modules | 12 | 3 |
| `modules/lazy_proxy.py` | Recording HTTP/HTTPS proxy for the autonomous loop. | modules | 68 | 5 |
| `modules/lazy_rbac.py` | modules/lazy_rbac.py | modules | 86 | 10 |
| `modules/lazy_reaper.py` | Reaper: expire lazy-loop tasks whose process proves dead. | modules | 3 | 2 |
| `modules/lazy_roles.py` | Lazy specialist roles for the autonomous loop. | modules | 4 | 2 |
| `modules/lazy_runner.py` | Single execution path for ``lazy_loop`` and ``auto_loop``. | modules | 51 | 17 |
| `modules/lazy_sandbox.py` | Per-task Docker sandbox for the Lazy autonomous loop. | modules | 12 | 2 |
| `modules/lazy_scope.py` | Lab-only default scope for autonomous loop targets. | modules | 17 | 1 |
| `modules/lazy_search.py` | Lazy saved-search grammar over the engagement database. | modules | 8 | 1 |
| `modules/lazy_sentinel.py` | Internal-network sentinel for LazyOwn. | modules | 12 | 0 |
| `modules/lazy_skill_mirror.py` | Mirror LazyOwn skills for Hermes discovery. | modules | 7 | 1 |
| `modules/lazy_skills.py` | Skill context injection for planner/worker prompts. | modules | 7 | 5 |
| `modules/lazy_summarizer.py` | Bounded chain summarizer for the Lazy autonomous loop. | modules | 5 | 0 |
| `modules/lazy_surface_diff.py` | Surface snapshot and diff: what changed about a host since last look. | modules | 9 | 0 |
| `modules/lazy_timeline.py` | Lazy engagement timeline for LazyOwn. | modules | 13 | 3 |
| `modules/lazy_triage.py` | Triage doctrine: evidence floors, verdict algebra and signature dedup. | modules | 10 | 1 |
| `modules/lazy_verify.py` | Structured read-only verification of loop findings. | modules | 8 | 0 |
| `modules/lazy_world_diff.py` | World-surface diff: host snapshots, change detection, ghost liveness. | modules | 22 | 7 |
| `modules/lazyatack.sh` | Nombre del script: lazyatack.sh Autor: Gris Iscomeback Correo electrónico... | modules | 30 | 0 |
| `modules/lazybrutesshuserenum.sh` | Función para manejar el interruptor de señal Ctrl+C | modules | 0 | 0 |
| `modules/lazyclonewars.sh` | Lista de repositorios (nombre y URL) | modules | 0 | 0 |
| `modules/lazycloud.py` | Cloud-native attack module for AWS, Azure, and GCP. | modules | 26 | 1 |
| `modules/lazycurl.sh` | Nombre del script: lazycurl.sh Autor: Gris Iscomeback Correo electrónico... | modules | 3 | 0 |
| `modules/lazydorks.py` | LazyDorks: target-aware Google and GitHub dork generator for LazyOwn. | modules | 4 | 0 |
| `modules/lazyencoder_decoder.py` | - | modules | 10 | 5 |
| `modules/lazyevilwimrm.sh` | execute_evil_winrm: Función para ejecutar evil-winrm y verificar la salida | modules | 1 | 0 |
| `modules/lazygat.sh` | Nombre del script: lazygath.sh Autor: Gris Iscomeback Correo electrónico... | modules | 0 | 0 |
| `modules/lazyk8s.py` | Container and Kubernetes attack module. | modules | 32 | 1 |
| `modules/lazylynis.sh` | Verificar si se proporcionó un argumento para el host remoto | modules | 1 | 0 |
| `modules/lazymasscan.sh` | Nombre del script: lazymasscan.sh Autor: Gris Iscomeback Correo electrónico... | modules | 4 | 0 |
| `modules/lazymobilerevshell.sh` | Verificar si se pasaron los argumentos de IP y puerto | modules | 0 | 0 |
| `modules/lazynmap.sh` | Nombre del script: lazynmap.sh Autor: Gris Iscomeback Correo electrónico... | modules | 8 | 0 |
| `modules/lazyown_bprfuzzer.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 15 | 0 |
| `modules/lazyown_bridge.py` | modules/lazyown_bridge.py | modules | 43 | 12 |
| `modules/lazyown_metaextract0r.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 9 | 0 |
| `modules/lazyown_parquet_tool.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 4 | 0 |
| `modules/lazyownerweb.py` | - | modules | 3 | 0 |
| `modules/lazypassgen.py` | LazyPassGen: target-aware weak-password generator for LazyOwn. | modules | 5 | 0 |
| `modules/lazypoophish.py` | LazyPoophish: phishing fallback delivery for the LazyOwn autonomous loop. | modules | 3 | 0 |
| `modules/lazypsexec.sh` | execute_psexec: Función para ejecutar psexec y verificar la salida | modules | 1 | 0 |
| `modules/lazyreverse_shell.sh` | Nombre del script: lazyreverse_shell.sh Autor: Gris Iscomeback Correo electrónico... | modules | 2 | 0 |
| `modules/lazyrtpflood.sh` | - | modules | 0 | 0 |
| `modules/lazyshortener.py` | LazyShortener: URL shortener bridge for LazyOwn phishing delivery. | modules | 2 | 1 |
| `modules/lazyvpnshield.sh` | Author: Nisrin Ahmed aka Wh1teDrvg0n Modify: grisun0 | modules | 7 | 0 |
| `modules/lazywps.sh` | - | modules | 1 | 0 |
| `modules/legacy/__init__.py` | Backward-compatibility shims for deprecated scripts. | misc | 0 | 0 |
| `modules/lesson_ingestor.py` | Lesson ingestion bridge between EpisodeReflectionEngine and MoERouter. | modules | 11 | 2 |
| `modules/lilsplunky.py` | Author: Your Name Email: youremail@example.com Creation Date: 14/04/2025 License: AGPL v3... | modules | 14 | 0 |
| `modules/linux_advanced_payloads.py` | Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants. | modules | 17 | 1 |
| `modules/listener_manager.py` | Multi-listener manager for LazyOwn C2. | modules | 22 | 2 |
| `modules/live_surface.py` | Live attack-surface graph derived from the world model. | modules | 7 | 3 |
| `modules/llm_adapter.py` | LLM adapter facade — single import point for all LLM backends used by lazyc2. | modules | 16 | 7 |
| `modules/llm_client.py` | LazyOwn Unified LLM Client | modules | 12 | 4 |
| `modules/llm_evaluator.py` | — Records LLM decisions and their outcomes, computes quality metrics, and exports fine-tuning... | modules | 28 | 2 |
| `modules/llm_factory.py` | LLM backend factory and selection utilities. | modules | 31 | 31 |
| `modules/llm_orchestrator.py` | Orchestrator-governed LLM failover chain for every AI module. | modules | 21 | 8 |
| `modules/llm_pool.py` | Ordered LLM failover pool with health-aware skipping. | modules | 20 | 9 |
| `modules/llm_prompts.py` | Canonical prompt-template and knowledge-base contract for LLM consumers. | modules | 28 | 5 |
| `modules/log_tamper.py` | Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log. | modules | 9 | 1 |
| `modules/logging_config.py` | Centralized logging configuration for the LazyOwn framework. | modules | 21 | 23 |
| `modules/loop/__init__.py` | - | loop | 0 | 7 |
| `modules/loop/decision_log.py` | Reproducible decision ledger for the autonomous loop. | loop | 10 | 0 |
| `modules/loop/engine_proxy.py` | EngineProxyMixin: Recorder-proxy lifecycle and traffic ingestion for the loop engine. | loop | 8 | 1 |
| `modules/loop/triage_scheduler.py` | Difficulty-triage scheduling for the autonomous multi-target loop. | loop | 11 | 3 |
| `modules/loop/worker_agentic.py` | WorkerAgenticMixin: Tool-calling agent loop and LLM step planning for a loop worker. | loop | 36 | 5 |
| `modules/loop/worker_execution.py` | WorkerExecutionMixin: Command execution, background jobs and persistent-shell lifecycle for a... | loop | 12 | 1 |
| `modules/loop/worker_gating.py` | WorkerGatingMixin: Scope, operating-system and privilege gates for a loop worker. | loop | 7 | 1 |
| `modules/loop/worker_memory.py` | WorkerMemoryMixin: Durable and in-session memory behaviour for a loop worker. | loop | 7 | 1 |
| `modules/loop_ai_bridge.py` | Single edge between the autonomous loop and the LazyOwn AI stack. | modules | 28 | 7 |
| `modules/loop_audit.py` | Operator audit trail for autonomous loop runs. | modules | 35 | 0 |
| `modules/loop_guardrails.py` | Adaptive guardrails for the autonomous loop. | modules | 49 | 9 |
| `modules/loop_limits.py` | Canonical operating limits for the autonomous loop. | modules | 0 | 3 |
| `modules/loop_manager.py` | Parallel autonomous loop orchestration for the LazyOwn C2 dashboard. | modules | 34 | 3 |
| `modules/loop_preflight.py` | Target and lab preflight checks for autonomous loops and auto_pwn. | modules | 6 | 0 |
| `modules/loop_progress.py` | Rich Live milestone panel for the autonomous loop. | modules | 15 | 4 |
| `modules/loop_triggers.py` | TriggerStore: persistent loop triggers extracted from the loop core. | modules | 16 | 8 |
| `modules/macos_payloads.py` | macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC. | modules | 16 | 1 |
| `modules/mario.py` | - | modules | 1 | 0 |
| `modules/mcp_agent_bridge.py` | LazyOwn MCP Agent Bridge | modules | 21 | 7 |
| `modules/mediation/__init__.py` | Mediation layer for LazyOwn cross-module coordination. | mediation | 0 | 5 |
| `modules/mediation/chain_mediator.py` | Specialised mediator for the APT chain pipeline. | mediation | 8 | 3 |
| `modules/mediation/contracts.py` | Mediation contracts: the abstractions every participant depends on. | mediation | 12 | 5 |
| `modules/mediation/engine_mediator.py` | Engine mediator: the loop's single coordination point to the engines. | mediation | 8 | 2 |
| `modules/mediation/feedback_mediator.py` | Specialised mediator for step-ordering feedback coordination. | mediation | 3 | 2 |
| `modules/mediation/hub.py` | Thin routing hub for specialised mediators. | mediation | 8 | 4 |
| `modules/mediation/intel_mediator.py` | specialised mediator for recon-intel coordination. | mediation | 9 | 2 |
| `modules/mediation/telemetry_mediator.py` | Specialised mediator for loop telemetry coordination. | mediation | 14 | 2 |
| `modules/memory_cleaner.py` | Memory artifact cleanup — process memory wipe, environment variable scrub, clipboard clear. | modules | 7 | 1 |
| `modules/memory_embeddings.py` | Hashing-trick text embeddings for episodic memory recall. | modules | 7 | 2 |
| `modules/memory_store.py` | — Episodic memory for the LazyOwn auto_loop. | modules | 38 | 1 |
| `modules/metasploitable_gym.py` | Metasploitable 2 gym catalogue loader and matrix validator. | modules | 9 | 3 |
| `modules/metasploitable_migrations.py` | Idempotent migrations for the Metasploitable 2 gym container. | modules | 5 | 2 |
| `modules/metrics.py` | LazyOwn metrics surface. | modules | 24 | 6 |
| `modules/mfa_bypass.py` | MFA Bypass Toolkit — techniques for circumventing multi-factor authentication. | modules | 10 | 1 |
| `modules/mkcloudflaretunnel.sh` | Download cloudflared and create a tunnel to localhost on a specified port. | modules | 0 | 0 |
| `modules/module_registry.py` | Unified module registry for LazyOwn — catalog, search, use/run workflow. | modules | 30 | 10 |
| `modules/moe_router.py` | modules/moe_router.py | modules | 39 | 6 |
| `modules/morse.py` | Morse code conversion service with interactive driver. | modules | 7 | 0 |
| `modules/mysql_hookandroot_lib.c` | reverse_shell: fork & send a bash shell to the attacker before starting mysqld | modules | 6 | 0 |
| `modules/network_opsec.py` | Network OPSEC — proxy chain enforcement, canary detection, traffic randomization. | modules | 12 | 1 |
| `modules/nmap2csv.py` | This file is part of nmaptocsv. | modules | 44 | 0 |
| `modules/nmap_fingerprint.py` | Canonical nmap XML fingerprinting for the exploit stack. | modules | 6 | 2 |
| `modules/notify.py` | Stateless multi-channel notifier for finding events. | modules | 17 | 7 |
| `modules/nuclei_templates_sync.py` | Sync community Nuclei template collections into the LazyOwn marketplace. | modules | 16 | 0 |
| `modules/obs_parser.py` | modules/obs_parser.py | modules | 42 | 10 |
| `modules/ooficesod0woodo.py` | LibreOffice UNO remote command execution stager. | modules | 1 | 0 |
| `modules/operation.py` | Caldera-style operation lifecycle: create, start, pause, resume, stop, status. | modules | 23 | 1 |
| `modules/operator_profiles.py` | Multi-operator profile management for LazyOwn team server. | modules | 20 | 1 |
| `modules/opsec_scorer.py` | OPSEC scoring engine — pre-execution noise assessment and gated scoring. | modules | 36 | 5 |
| `modules/orchestrator_config.py` | Operator configuration for the loop core: profiles, stages and auto verbs. | modules | 41 | 21 |
| `modules/osint_enrich.py` | Keyless OSINT enrichment for finding evidence. | modules | 13 | 2 |
| `modules/outcome_attribution.py` | Observer-style failure attribution for autonomous loop steps. | modules | 10 | 3 |
| `modules/outcome_bus.py` | Single fan-out contract for engagement outcomes. | modules | 17 | 38 |
| `modules/payload_factory.py` | Native payload generation framework — stagers, stages, singles, formats. | modules | 32 | 7 |
| `modules/phishing_orchestrator.py` | Smart Phishing Campaign Orchestrator. | modules | 23 | 3 |
| `modules/pipeline_engine.py` | modules/pipeline_engine.py — Declarative YAML pipelines for LazyOwn | modules | 80 | 8 |
| `modules/planner.py` | Fact-based planner — decides the next ability to run. | modules | 28 | 7 |
| `modules/playbook_admin.py` | Safe CRUD for the YAML playbooks under ``playbooks/``. | modules | 18 | 3 |
| `modules/playbook_chain.py` | Playbook to chain lowering: one contract, one destination. | modules | 5 | 2 |
| `modules/playbook_engine.py` | modules/playbook_engine.py | modules | 32 | 10 |
| `modules/playbook_executor.py` | Playbook Executor — bridges MITRE ATT&CK playbooks to the pipeline engine. | modules | 25 | 0 |
| `modules/poc_registry.py` | Reusable PoC verbs: standalone exploit scripts as loop-routable actions. | modules | 16 | 0 |
| `modules/polymorphic_engine.py` | Polymorphic code generation engine — shellcode mutation and obfuscation. | modules | 19 | 1 |
| `modules/privesc_predictor.py` | Crystal Ball — privilege escalation vector prediction engine. | modules | 17 | 1 |
| `modules/professional_report.py` | Professional Red Team Report Generator. | modules | 24 | 3 |
| `modules/progress_ledger.py` | Objective-progress ledger: qualitative strikes against goal stagnation. | modules | 17 | 2 |
| `modules/r.sh` | Obtener la versión del kernel actual | modules | 1 | 9 |
| `modules/reaction_bridge.py` | Reaction bridge between the reactive engine and the loop planner. | modules | 9 | 3 |
| `modules/reactive_engine.py` | modules/reactive_engine.py | modules | 42 | 10 |
| `modules/recommender.py` | LazyOwn Smart Command Recommender | modules | 4 | 2 |
| `modules/redteam_gym.py` | Red Team Gym — gamified pentest training mode. | modules | 30 | 8 |
| `modules/reflective_dll.py` | Reflective DLL loading — load PE from memory without touching disk. | modules | 27 | 0 |
| `modules/resource_script.py` | Enhanced resource script engine — variables, conditionals, loops, macros. | modules | 21 | 3 |
| `modules/retry_session.py` | Retry sessions - safely relaunch a failed verb or a failed run. | modules | 10 | 3 |
| `modules/reverse-shell.c` | reverse_shell_init: call_usermodehelper function is used to create user mode processes from... | modules | 2 | 0 |
| `modules/revshell.c` | - | modules | 2 | 0 |
| `modules/rich_tui.py` | Rich-based live TUI dashboard for LazyOwn campaign monitoring. | modules | 14 | 1 |
| `modules/rl_trainer.py` | modules/rl_trainer.py | modules | 31 | 5 |
| `modules/rootkit/mr.c` | - | rootkit | 33 | 0 |
| `modules/rootkit/mrhyde.c` | original_dirent: ifndef HIDE_DIR define HIDE_DIR ".rootkit_dir" endif ifndef HIDE_USER define... | rootkit | 38 | 0 |
| `modules/rootkit/mrhyde2.c` | original_dirent: ifndef HIDE_DIR define HIDE_DIR ".rootkit_dir" endif ifndef HIDE_USER define... | rootkit | 35 | 0 |
| `modules/rootkit/mrhyde3.c` | io_uring_sq: #endif #ifndef HIDE_USER #define HIDE_USER "rootkit_user" #endif #define... | rootkit | 57 | 0 |
| `modules/rootkit/rootkit.asm` | - | rootkit | 1 | 0 |
| `modules/rootkit/rootkit.c` | Define the process name and file name to hide Operable values are provided via the Makefile... | rootkit | 13 | 0 |
| `modules/saas_attacks.py` | SaaS attacks — Microsoft 365, Google Workspace, Salesforce, ServiceNow exploitation. | modules | 15 | 1 |
| `modules/scan_brief.py` | Scan brief: sharpen loop probes against services an nmap scan already found. | modules | 10 | 3 |
| `modules/scripts/clean_history.sh.sh` | - | misc | 0 | 0 |
| `modules/search.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 0 | 1 |
| `modules/security_sanitizers.py` | Security sanitizers shared across the LazyOwn framework. | modules | 25 | 5 |
| `modules/selection/__init__.py` | Shared action-selection brain for the unified autonomous loop. | selection | 0 | 3 |
| `modules/selection/_phase_categories.py` | Shared kill-chain-phase to lookup-category mapping. | selection | 1 | 2 |
| `modules/selection/adversary.py` | Adversary selector: run a custom adversary emulation named by the objective. | selection | 6 | 3 |
| `modules/selection/atomic.py` | Atomic selector: emulate named MITRE ATT&CK techniques with atomic tests. | selection | 2 | 5 |
| `modules/selection/base.py` | The one shared contract for autonomous action selection. | selection | 4 | 32 |
| `modules/selection/bridge.py` | Bridge selector: propose a phase/service-appropriate catalogued command. | selection | 2 | 3 |
| `modules/selection/chain.py` | Chain selector: propose a vetted ``apt_chain`` when one fits the state. | selection | 3 | 5 |
| `modules/selection/cred_spray.py` | Credential-spray selector: reuse known credentials against open services. | selection | 2 | 3 |
| `modules/selection/edb.py` | EDBSelector: Propose ExploitDB (atomic_exploit) when services/cves fit. | selection | 2 | 1 |
| `modules/selection/intel.py` | Intel selector: feed exploitation intelligence into the autonomous loop. | selection | 7 | 3 |
| `modules/selection/lazyscript.py` | Lazyscript selector: propose an operator-authored .ls recipe when it fits. | selection | 5 | 2 |
| `modules/selection/module.py` | Module selector: map goal/service mentions onto runnable registry modules. | selection | 2 | 5 |
| `modules/selection/parquet.py` | Parquet selector: propose the command that most often succeeded before. | selection | 4 | 5 |
| `modules/selection/playbook.py` | Playbook selector: run an APT actor emulation named by the objective. | selection | 7 | 3 |
| `modules/selection/poc.py` | PoC selector: propose catalogued PoC verbs when services match. | selection | 2 | 3 |
| `modules/selection/registry.py` | Assemble and run the shared selector cascade. | selection | 3 | 8 |
| `modules/selection/technique.py` | Technique selector: propose MITRE technique emulation for the phase. | selection | 2 | 2 |
| `modules/selection/technique_chain.py` | Technique-chain selector: compile the phase's techniques into one paced chain. | selection | 3 | 2 |
| `modules/selector_manager.py` | Selector manager: deterministic priority cascade with provenance. | modules | 3 | 1 |
| `modules/selfupdate.py` | Guarded self-update for the LazyOwn working tree. | modules | 12 | 4 |
| `modules/service_aliases.py` | Service alias knowledge for the matching surfaces. | modules | 0 | 3 |
| `modules/session_cleanup.py` | Ephemeral infrastructure cleanup on shell exit. | modules | 5 | 2 |
| `modules/session_rag.py` | — ChromaDB-backed RAG over sessions/ artefacts. | modules | 24 | 7 |
| `modules/session_reader.py` | modules/session_reader.py | modules | 29 | 4 |
| `modules/session_state.py` | LazyOwn Session State | modules | 9 | 1 |
| `modules/sidequest.py` | Read-only side questions against the loop's immutable decision checkpoints. | modules | 6 | 0 |
| `modules/sidequestion.py` | Isolated side-question answering against immutable snapshots. | modules | 9 | 2 |
| `modules/sinks/__init__.py` | Outcome sink adapters. | sinks | 0 | 2 |
| `modules/sinks/attack_graph.py` | Attack-graph sink: rebuild the attack surface after meaningful outcomes. | sinks | 1 | 1 |
| `modules/sinks/beacon_dispatch.py` | Beacon dispatch sink: on a foothold, stage the catch-back command. | sinks | 3 | 1 |
| `modules/sinks/c2_surfaces.py` | C2 dashboard sink: banners, CVEs and operator notes. | sinks | 1 | 1 |
| `modules/sinks/campaign_db.py` | Campaign database sink: opt-in host and vulnerability mirror. | sinks | 1 | 0 |
| `modules/sinks/chain_feed.py` | Chain-feed sink: stream chain steps into the autonomous loop. | sinks | 1 | 2 |
| `modules/sinks/event_bus.py` | Unified event-bus sink: publish every outcome once. | sinks | 1 | 0 |
| `modules/sinks/findings.py` | Findings sink: append engagement finding transitions to the ledger. | sinks | 5 | 3 |
| `modules/sinks/intel_graph.py` | Intel-graph sink: rebuild the fused graph after meaningful outcomes. | sinks | 1 | 1 |
| `modules/sinks/killchain.py` | Kill-chain sink: advance the unified phase from proven outcomes. | sinks | 1 | 1 |
| `modules/sinks/lazy_intel.py` | Lazy intel sink: mirror exploit-intelligence matches into the stores. | sinks | 3 | 0 |
| `modules/sinks/objectives.py` | Objectives sink: turn proven outcomes into follow-up work. | sinks | 1 | 1 |
| `modules/sinks/routing.py` | Routing-prior sink: learn from terminal outcomes. | sinks | 1 | 1 |
| `modules/sinks/world_diff.py` | World-diff sink: snapshot hosts and record what changed per outcome. | sinks | 4 | 2 |
| `modules/sinks/world_model.py` | World-model sink: hosts, services, vulnerabilities and credentials. | sinks | 1 | 0 |
| `modules/sleep_obfuscation.py` | Sleep obfuscation engine for beacon memory evasion. | modules | 28 | 3 |
| `modules/smbver.sh` | Author: rewardone Description: Requires root or enough permissions to use tcpdump Will listen... | modules | 0 | 0 |
| `modules/socks_proxy.py` | SOCKS5 proxy engine for tunneling traffic through LazyOwn beacons. | modules | 31 | 3 |
| `modules/staged_delivery.py` | Staged payload delivery — HTA, Office macros, LNK files, ISO/VHD packaging. | modules | 18 | 1 |
| `modules/state_manager.py` | UnifiedStateManager — single source of truth for all LazyOwn campaign state. | modules | 44 | 8 |
| `modules/stego_video.py` | Video steganography addon for LazyOwn. | modules | 10 | 0 |
| `modules/sudo_tiocsti.py` | – Production‑grade TIOCSTI injection with multiple attack modes. | modules | 9 | 0 |
| `modules/surface_ops.py` | Pure attack-surface helpers (no cmd2): discovery targets, confirm parsing. | modules | 4 | 2 |
| `modules/test_lazyencoder_decoder.py` | - | modules | 0 | 0 |
| `modules/threat_model.py` | — Blue team threat model builder for LazyOwn. | modules | 16 | 1 |
| `modules/timeline_narrator.py` | LazyOwn Timeline Narrator | modules | 6 | 4 |
| `modules/timestomper.py` | Filesystem timestomping — MACB timestamp manipulation for stealth. | modules | 12 | 1 |
| `modules/tmp.sh` | - | modules | 0 | 0 |
| `modules/tools/__init__.py` | Reusable development tools for the LazyOwn autonomous loop. | modules_tools | 0 | 1 |
| `modules/tools/loop_smoke.py` | End-to-end smoke of the shared loop runner (no LLM, no network). | modules_tools | 10 | 0 |
| `modules/tools/monitor_smoke.py` | Headless smoke of the Textual worker monitor (``lazy_view``). | modules_tools | 3 | 0 |
| `modules/toolset.py` | Typed tool sets per agent role with shell allowlists. | modules | 5 | 1 |
| `modules/toposwarm_bridge.py` | modules/toposwarm_bridge.py | modules | 22 | 6 |
| `modules/traffic_morpher.py` | C2 traffic obfuscation: domain fronting, protocol mimicking, and traffic shaping. | modules | 11 | 1 |
| `modules/traffic_recorder.py` | HTTP traffic recorder with file-tree storage and SQLite index. | modules | 23 | 12 |
| `modules/trigger_policy.py` | Declarative trigger policy: YAML seeds for the loop TriggerStore. | modules | 8 | 8 |
| `modules/ttp_coverage.py` | TTP coverage matrix — real-time MITRE ATT&CK technique tracking. | modules | 13 | 1 |
| `modules/ttpscope_bridge.py` | Secure bridge for the TTPScope MITRE ATT&CK research client. | modules | 33 | 1 |
| `modules/unified_bridge.py` | UnifiedBridge — single API over all LazyOwn bridges and routing engines. | modules | 29 | 1 |
| `modules/unified_dashboard.py` | Unified campaign dashboard — combines all state sources into one view. | modules | 15 | 2 |
| `modules/update_db.sh` | Nombre del script: update_db.sh Autor: Gris Iscomeback Correo electrónico... | modules | 0 | 0 |
| `modules/venator.py` | - | modules | 34 | 0 |
| `modules/verb_catalog.py` | Operator-owned YAML catalog of every routable shell verb. | modules | 21 | 10 |
| `modules/verb_manifest.py` | Typed verb manifests - semantics for routable shell verbs. | modules | 17 | 3 |
| `modules/vuln_bot_cli.py` | - | modules | 2 | 0 |
| `modules/vulnbot.py` | list_files: Lista archivos en un directorio | modules | 23 | 2 |
| `modules/websocket_beacon.py` | WebSocket beacon transport for modern C2 channels. | modules | 21 | 0 |
| `modules/win_rootkit/backup.c` | - | win_rootkit | 17 | 0 |
| `modules/win_rootkit/mrhyde.c` | RunExperiment: Define the RunExperiment function | win_rootkit | 18 | 0 |
| `modules/win_rootkit/win_rin3_rootkit.cs` | - | win_rootkit | 10 | 0 |
| `modules/win_rootkit/win_ring3_rootkit.c` | initPIDArray: Función para inicializar el arreglo de PIDs | win_rootkit | 27 | 0 |
| `modules/win_rootkit/win_ring3_rootkit.cpp` | - | win_rootkit | 9 | 0 |
| `modules/winbox_gym.py` | WinBox gym catalogue and control-plane bridge. | modules | 38 | 0 |
| `modules/wineconfig.sh` | - | modules | 0 | 0 |
| `modules/wire_capture.py` | Durable byte-for-byte capture of a traffic exchange's raw output. | modules | 9 | 2 |
| `modules/workspace.py` | Confined workspace file browser for operators and loop agents. | modules | 7 | 1 |
| `modules/world_model.py` | modules/world_model.py | modules | 70 | 82 |
| `modules/yaml_generator.py` | load_payload: Carga las variables desde payload.json (canonical loader). | modules | 8 | 0 |
| `modules/yara_scanner.py` | YARA integration for malware classification and IOC scanning. | modules | 16 | 2 |
| `mutate.sh` | - | root | 0 | 0 |
| `plugins/generate_c_reverse_shell.lua` | - | plugins | 2 | 0 |
| `plugins/generate_cleanup_commands.lua` | - | plugins | 1 | 0 |
| `plugins/generate_html_payload.lua` | - | plugins | 1 | 0 |
| `plugins/generate_lateral_command.lua` | - | plugins | 1 | 0 |
| `plugins/generate_linux_asm_reverse_shell.lua` | - | plugins | 2 | 0 |
| `plugins/generate_linux_raw_shellcode.lua` | - | plugins | 1 | 0 |
| `plugins/generate_lolbird.lua` | - | plugins | 6 | 0 |
| `plugins/generate_msfvenom_loader.lua` | - | plugins | 5 | 0 |
| `plugins/generate_msfvenom_loader_windows.lua` | - | plugins | 1 | 0 |
| `plugins/generate_reverse_shell.lua` | - | plugins | 1 | 0 |
| `plugins/generate_stub.lua` | - | plugins | 5 | 0 |
| `plugins/init_plugins.lua` | - | plugins | 1 | 0 |
| `plugins/kerberos_harvest.lua` | - | plugins | 1 | 0 |
| `plugins/lolbas_bitsadmin_exe.lua` | - | plugins | 0 | 0 |
| `plugins/lolbas_certutil_download_exec.lua` | - | plugins | 3 | 0 |
| `plugins/lolbas_certutil_exe.lua` | - | plugins | 1 | 0 |
| `plugins/lolbas_mshta_js.lua` | - | plugins | 0 | 0 |
| `plugins/lolbas_mshta_reverse_shell.lua` | - | plugins | 0 | 0 |
| `plugins/lolbas_rundll32_dll.lua` | - | plugins | 0 | 0 |
| `plugins/lolbas_wmic_xsl_execution.lua` | - | plugins | 1 | 0 |
| `plugins/parse_nmap_with_xmlstarlet.lua` | - | plugins | 1 | 0 |
| `plugins/run_nuclei_on_nmap_files.lua` | - | plugins | 1 | 0 |
| `plugins/run_python_rev_c2.lua` | - | plugins | 1 | 0 |
| `plugins/rundll32_sct_from_url.lua` | - | plugins | 4 | 0 |
| `plugins/validate_shellcode.lua` | - | plugins | 4 | 0 |
| `plugins/visualize_network.lua` | - | plugins | 1 | 0 |
| `poc_tui/__main__.py` | Entry point: python3 -m poc_tui | poc_tui | 0 | 0 |
| `poc_tui/app.py` | LazyOwn TUI Shell — Proof of Concept.  cmd2 as backend, Textual as frontend. | poc_tui | 47 | 3 |
| `poc_tui/config.py` | Payload.json configuration manager for the TUI shell. | poc_tui | 11 | 1 |
| `poc_tui/plugin_loader.py` | Unified plugin loader — YAML addons, Lua plugins, and .tool files. | poc_tui | 22 | 0 |
| `poc_tui/run.py` | Convenience launcher that symlinks LazyOwn dirs and starts the TUI. | poc_tui | 1 | 1 |
| `poc_tui/test_app.py` | Pytest tests for LazyOwn TUI Shell POC. | poc_tui | 56 | 0 |
| `pwntomate.py` | This software must not be used by military or secret service organisations. | root | 3 | 0 |
| `py2elf.sh` | Nombre del script: py2elf.sh Autor: Gris Iscomeback Correo electrónico... | root | 0 | 0 |
| `readmeneitor.py` | — Automated documentation generator for LazyOwn RedTeam Framework. | root | 11 | 0 |
| `run_telegram_hermes.sh` | Launcher for telegram_hermes.py Uses the dedicated venv with python-telegram-bot dependencies | root | 0 | 0 |
| `run_topoexploit_agent.sh` | Run TopoExploit against an ExploitGym task using the local model. | root | 2 | 0 |
| `scripts/__init__.py` | Repository-side maintenance scripts. | scripts | 0 | 0 |
| `scripts/activate_migrations.py` | Activate dormant CommandSet migrations. | scripts | 7 | 0 |
| `scripts/backfill_addon_os_trigger.py` | One-shot backfill: add ``os`` and ``trigger`` keys to every lazyaddon. | scripts | 5 | 0 |
| `scripts/broadcom_wps_drive.sh` | operator-side driver for the Broadcom 802.11 SDK detection toolkit. | scripts | 25 | 0 |
| `scripts/check_contract_manifest.py` | Verify that documented contracts still exist on disk. | scripts | 13 | 1 |
| `scripts/devtools/command_audit.py` | Audit every registered shell command for dispatch and parser errors. | devtools | 4 | 0 |
| `scripts/devtools/core_smoke.py` | Smoke check for the public surfaces documented in CORE.md. | devtools | 4 | 0 |
| `scripts/dirtyinit_drive.sh` | operator-side driver for the DirtyInit Android root chain. | scripts | 28 | 0 |
| `scripts/fix_migrated_classes.py` | - | scripts | 0 | 0 |
| `scripts/generate_sbom.py` | Generate a minimal CycloneDX SBOM from the pinned requirements files. | scripts | 5 | 0 |
| `scripts/journal.py` | Read-before-you-write journal over GitHub Discussions. | scripts | 14 | 2 |
| `scripts/lazy_hermes_ask.sh` | — detached Hermes task runner for LazyOwn. | scripts | 0 | 0 |
| `scripts/lazy_llamacpp_serve.sh` | — idempotent llama.cpp server manager for LazyOwn. | scripts | 1 | 0 |
| `scripts/lazy_llamacpp_setup.sh` | — one-time local LLM setup for LazyOwn users. | scripts | 1 | 0 |
| `scripts/lazy_msf_lab.sh` | — Metasploitable2 smoke lab manager for LazyOwn. | scripts | 0 | 0 |
| `scripts/lazy_opencode_config.py` | Patch operator agent configs to use the Lazy llama.cpp server. | scripts | 6 | 1 |
| `scripts/mcp_call.py` | Call one LazyOwn MCP tool over stdio and print its text content. | scripts | 9 | 0 |
| `scripts/migrate_commandsets.py` | Merge _migrated.py CommandSet methods into clean phase modules. | scripts | 6 | 0 |
| `scripts/migrate_lazyown.py` | Staged migration script: extract do_* methods from lazyown.py into cli/commands/. | scripts | 6 | 1 |
| `scripts/mutate.sh` | Mutation gate for LazyOwn. | scripts | 3 | 0 |
| `scripts/mutation_gate.py` | Consolidated mutation gate for LazyOwn. | scripts | 3 | 0 |
| `scripts/patch_playbook_atomic_ids.py` | Patch APT playbooks: replace placeholder atomic_ids with real technique_ids. | scripts | 0 | 0 |
| `scripts/pi_qwen_setup.sh` | idempotent bootstrap for the pi_qwen lazyaddon. | scripts | 0 | 0 |
| `scripts/publish_wiki.sh` | Publish LazyOwn documentation to the GitHub wiki. | scripts | 8 | 0 |
| `scripts/read_journal.py` | Print the recent engineering journal before a change is written. | scripts | 2 | 0 |
| `scripts/setup_hermes_mcp.sh` | — register LazyOwn MCP server in Hermes Agent config Usage: bash scripts/setup_hermes_mcp.sh... | scripts | 0 | 0 |
| `scripts/smoke_onboarding.sh` | Smoke test for the 5-minute onboarding path. | scripts | 1 | 0 |
| `scripts/sync_doc_stats.py` | Sync documentation numbers with the live codebase — single source of truth. | scripts | 6 | 0 |
| `scripts/test_bdd.sh` | Behavior-driven (BDD) suite gate for LazyOwn. | scripts | 2 | 0 |
| `scripts/top_tier_check.py` | Top-tier hygiene audit for LazyOwn. | scripts | 10 | 0 |
| `scripts/update_apt_atomic_ids.py` | Update APT playbooks with real Atomic Red Team test IDs. | scripts | 2 | 0 |
| `scripts/validate_agent_contract.sh` | CI validation of the AGENTS.md branching model and coding standards. | scripts | 5 | 0 |
| `setup.py` | Compatibility shim for legacy ``python setup.py`` invocations. | root | 0 | 0 |
| `skills/aci_planner.py` | Autonomous Campaign Intelligence (ACI) Planner | skills | 42 | 5 |
| `skills/autonomous_daemon.py` | skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon | skills | 142 | 25 |
| `skills/autonomous_replay.py` | Deterministic replay of past autonomous-daemon runs. | skills | 19 | 1 |
| `skills/claude_md_orchestrator/__init__.py` | Public API for the claude_md_orchestrator skill. | claude_md_orchestrator | 0 | 1 |
| `skills/claude_md_orchestrator/bdd_agent.py` | Behavior-Driven Development agent. | claude_md_orchestrator | 8 | 0 |
| `skills/claude_md_orchestrator/boy_scout.py` | Boy Scout refactor pass. | claude_md_orchestrator | 5 | 0 |
| `skills/claude_md_orchestrator/cicd_agent.py` | CI and CD agent. | claude_md_orchestrator | 7 | 0 |
| `skills/claude_md_orchestrator/config.py` | Centralized configuration for the claude_md_orchestrator skill. | claude_md_orchestrator | 15 | 10 |
| `skills/claude_md_orchestrator/documentation_agent.py` | Documentation agent. | claude_md_orchestrator | 7 | 0 |
| `skills/claude_md_orchestrator/models.py` | Data models for the claude_md_orchestrator skill. | claude_md_orchestrator | 32 | 11 |
| `skills/claude_md_orchestrator/orchestrator.py` | Orchestrator that wires the agents into a deterministic pipeline. | claude_md_orchestrator | 21 | 1 |
| `skills/claude_md_orchestrator/parser.py` | Parser that turns a CLAUDE.md into actionable contracts. | claude_md_orchestrator | 13 | 4 |
| `skills/claude_md_orchestrator/reviewer_agent.py` | Code Reviewer and Quality Assurance agent. | claude_md_orchestrator | 10 | 0 |
| `skills/claude_md_orchestrator/sdd_agent.py` | Spec-Driven Development agent. | claude_md_orchestrator | 6 | 0 |
| `skills/claude_md_orchestrator/tdd_agent.py` | Test-Driven Development agent. | claude_md_orchestrator | 7 | 1 |
| `skills/claude_md_orchestrator/tests/conftest.py` | Pytest bootstrap for the claude_md_orchestrator test suite. | skills_claude_md_orchestrator_tests | 0 | 0 |
| `skills/claude_md_orchestrator/tests/test_orchestrator.py` | Unit tests for the claude_md_orchestrator package. | skills_claude_md_orchestrator_tests | 20 | 0 |
| `skills/claude_md_orchestrator/validators.py` | DoD validators for every artifact the orchestrator produces. | claude_md_orchestrator | 21 | 6 |
| `skills/daemon_control.py` | Operator steering layer for the LazyOwn autonomous daemon. | skills | 27 | 10 |
| `skills/daemon_health.py` | Daemon health monitor — watchdog for the autonomous daemon and C2 listeners. | skills | 16 | 1 |
| `skills/heartbeat.py` | LazyOwn Heartbeat | skills | 5 | 0 |
| `skills/hermes-lazyown/__init__.py` | Hermes-LazyOwn integration package. | hermes-lazyown | 0 | 0 |
| `skills/hermes-lazyown/claudemd_rules.py` | Dynamic Claude.md rule generator for the Hermes-LazyOwn integration. | hermes-lazyown | 14 | 1 |
| `skills/hermes-lazyown/config_bridge.py` | Configuration bridge: unifies LazyOwn payload.json, environment variables, and fallback defaults... | hermes-lazyown | 16 | 1 |
| `skills/hermes-lazyown/constants.py` | Central constants for the Hermes-LazyOwn integration layer. | hermes-lazyown | 15 | 6 |
| `skills/hermes-lazyown/executor.py` | LazyOwn command executor for the Hermes-LazyOwn integration. | hermes-lazyown | 13 | 1 |
| `skills/hermes-lazyown/hermes_sync.py` | Hermes-native synchronization layer. | hermes-lazyown | 14 | 1 |
| `skills/hermes-lazyown/mcp_server.py` | Hermes-native MCP server for LazyOwn. | hermes-lazyown | 28 | 0 |
| `skills/hermes-lazyown/output_compactor.py` | Phase-aware output compaction for the Hermes-LazyOwn integration. | hermes-lazyown | 20 | 1 |
| `skills/hive_mind.py` | skills/hive_mind.py — LazyOwn Borg Hive Mind | skills | 107 | 14 |
| `skills/lazyown_automapper.py` | LazyOwn MCP Auto-Mapper | skills | 23 | 1 |
| `skills/lazyown_campaign.py` | LazyOwn CampaignStore | skills | 26 | 1 |
| `skills/lazyown_claudemd.py` | LazyOwn CLAUDE.md Hierarchical Loader (Claude Code style)  4-level hierarchy (highest → lowest... | skills | 8 | 2 |
| `skills/lazyown_context.py` | LazyOwn Context Compaction Pipeline — 5-layer graduated compression (Claude Code style)  Layers: 1. | skills | 11 | 3 |
| `skills/lazyown_daemon.py` | LazyOwn Unified Daemon | skills | 24 | 0 |
| `skills/lazyown_facts.py` | LazyOwn FactStore | skills | 79 | 13 |
| `skills/lazyown_groq_agents.py` | skills/lazyown_groq_agents.py | skills | 40 | 4 |
| `skills/lazyown_hooks.py` | LazyOwn Hook Pipeline (Claude Code style)  8 lifecycle events with chainable handlers. | skills | 14 | 2 |
| `skills/lazyown_llm.py` | LazyOwn LLM Bridge — MCP Edition | skills | 21 | 5 |
| `skills/lazyown_mcp.py` | LazyOwn MCP Server Exposes LazyOwn framework capabilities as MCP tools for Claude Code and... | skills | 61 | 9 |
| `skills/lazyown_mcp_helpers.py` | LazyOwn MCP helper functions — pure logic, no MCP server imports. | skills | 21 | 12 |
| `skills/lazyown_mcp_opencode.py` | LazyOwn MCP OpenCode bridge. | skills | 6 | 1 |
| `skills/lazyown_objective.py` | LazyOwn Objective Store | skills | 36 | 12 |
| `skills/lazyown_parquet_db.py` | LazyOwn Parquet Knowledge Base | skills | 21 | 11 |
| `skills/lazyown_permissions.py` | LazyOwn Permission System — Deny-First Rule Evaluation (Claude Code style)  Deny rules ALWAYS... | skills | 16 | 2 |
| `skills/lazyown_policy.py` | LazyOwn Policy Engine | skills | 126 | 10 |
| `skills/lazyown_session.py` | LazyOwn Append-Only Session Transcripts (Claude Code style)  All writes are append-only JSONL. | skills | 14 | 4 |
| `skills/mcp_generated_tools.py` | Auto-generated MCP tool handlers from command_index.json. | skills | 645 | 0 |
| `skills/mcp_lazy.py` | Single helper behind every lazy optional import of the MCP server. | skills | 1 | 2 |
| `skills/mcp_restart.sh` | LazyOwn MCP restart helper  Kills ALL lazyown_mcp instances (stdio + SSE) and relaunches the SSE... | skills | 0 | 0 |
| `skills/mcp_tool_generator.py` | Auto-generate MCP tool handlers from cli/command_index.json. | skills | 9 | 0 |
| `skills/mcp_tools/__init__.py` | Auto-discovered one-file-per-tool registry for the LazyOwn MCP server. | mcp_tools | 5 | 1 |
| `skills/mcp_tools/_context.py` | Dependency-injection context handed to every ``mcp_tools`` handler. | mcp_tools | 1 | 190 |
| `skills/mcp_tools/aci_plan.py` | MCP tool ``lazyown_aci_plan`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/aci_replan.py` | MCP tool ``lazyown_aci_replan`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/aci_status.py` | MCP tool ``lazyown_aci_status`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/ack_event.py` | MCP tool ``lazyown_ack_event``: mark an event as processed. | mcp_tools | 1 | 0 |
| `skills/mcp_tools/add_rule.py` | MCP tool ``lazyown_add_rule`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/add_target.py` | MCP tool ``lazyown_add_target`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/agent_result.py` | MCP tool ``lazyown_agent_result`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/agent_status.py` | MCP tool ``lazyown_agent_status`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/apt_chain.py` | MCP tool ``lazyown_apt_chain`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/atomic_clean.py` | MCP tool ``lazyown_atomic_clean`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/atomic_resolve.py` | MCP tool ``lazyown_atomic_resolve`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/atomic_search.py` | MCP tool ``lazyown_atomic_search`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/atomic_shell.py` | MCP tool ``lazyown_atomic_shell`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/auto_loop.py` | MCP tool ``lazyown_auto_loop`` (single runner, one path with the CLI). | mcp_tools | 3 | 1 |
| `skills/mcp_tools/auto_populate.py` | MCP tool ``lazyown_auto_populate`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/auto_pwn.py` | MCP tool ``lazyown_auto_pwn``: run the full autonomous exploitation chain. | mcp_tools | 1 | 0 |
| `skills/mcp_tools/autonomous_events.py` | MCP tool ``lazyown_autonomous_events`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/autonomous_inject.py` | MCP tool ``lazyown_autonomous_inject`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/autonomous_replay.py` | MCP tool ``lazyown_autonomous_replay`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/autonomous_start.py` | MCP tool ``lazyown_autonomous_start`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/autonomous_status.py` | MCP tool ``lazyown_autonomous_status`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/autonomous_stop.py` | MCP tool ``lazyown_autonomous_stop`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/bridge_suggest.py` | MCP tool ``lazyown_bridge_suggest`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/c2_adversary.py` | MCP tool ``lazyown_c2_adversary`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/c2_command.py` | MCP tool ``lazyown_c2_command`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/c2_notes.py` | MCP tool ``lazyown_c2_notes`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/c2_profile.py` | MCP tool ``lazyown_c2_profile`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/c2_redop.py` | MCP tool ``lazyown_c2_redop`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/c2_script.py` | MCP tool ``lazyown_c2_script`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/c2_search_agent.py` | MCP tool ``lazyown_c2_search_agent`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/c2_status.py` | MCP tool ``lazyown_c2_status``: check C2 reachability and dashboard data. | mcp_tools | 1 | 0 |
| `skills/mcp_tools/c2_vuln_analysis.py` | MCP tool ``lazyown_c2_vuln_analysis`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/campaign.py` | MCP tool ``lazyown_campaign`` (migrated from the call_tool dispatch chain). | mcp_tools | 2 | 0 |
| `skills/mcp_tools/campaign_lessons.py` | MCP tool ``lazyown_campaign_lessons`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/campaign_sitrep.py` | MCP tool ``lazyown_campaign_sitrep`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/campaign_tasks.py` | MCP tool ``lazyown_campaign_tasks`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/claudemd.py` | MCP tool ``lazyown_claudemd`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/collab_publish.py` | MCP tool ``lazyown_collab_publish`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/command_help.py` | MCP tool ``lazyown_command_help`` (migrated from the call_tool dispatch chain). | mcp_tools | 2 | 0 |
| `skills/mcp_tools/command_next.py` | MCP tool ``lazyown_command_next`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/command_prev.py` | MCP tool ``lazyown_command_prev`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/create_addon.py` | MCP tool ``lazyown_create_addon`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/create_param.py` | MCP tool ``lazyown_create_param`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/create_tool.py` | MCP tool ``lazyown_create_tool`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/credentials.py` | MCP tool ``lazyown_credentials``: aggregate captured credentials. | mcp_tools | 2 | 0 |
| `skills/mcp_tools/cron_schedule.py` | MCP tool ``lazyown_cron_schedule`` (migrated from the call_tool dispatch chain). | mcp_tools | 3 | 0 |
| `skills/mcp_tools/cve_search.py` | MCP tool ``lazyown_cve_search`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/daemon.py` | MCP tool ``lazyown_daemon`` (migrated from the call_tool dispatch chain). | mcp_tools | 2 | 0 |
| `skills/mcp_tools/daemon_approve.py` | MCP tool ``lazyown_daemon_approve`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/daemon_focus.py` | MCP tool ``lazyown_daemon_focus`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/daemon_mode.py` | MCP tool ``lazyown_daemon_mode`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/daemon_pause.py` | MCP tool ``lazyown_daemon_pause`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/daemon_resume.py` | MCP tool ``lazyown_daemon_resume`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/daemon_status.py` | MCP tool ``lazyown_daemon_status`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/daemon_veto.py` | MCP tool ``lazyown_daemon_veto`` (migrated from the call_tool dispatch chain). | mcp_tools | 1 | 0 |
| `skills/mcp_tools/dashboard_snapshot.py` | MCP tool ``lazyown_dashboard_snapshot``: render the live network map. | mcp_tools | 1 | 0 |

Next: [INDEX_p3.md](INDEX_p3.md)
