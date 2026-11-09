# Second Brain

*Last synthesized: 2026-11-09 | 1345 files | 30 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `lazy_loop.py`, `utils.py`. Architecturally it is 6 layers, dominant utility (780 files) across 30 import-based communities. Recorded risk surface: 0 security findings and 141 dependency cycles.

Surprising tissue lives between modules: autonomous_daemon, cli/commands, modules: lazy_loop: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (90% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1345 |
| Symbols | 24242 |
| Resolved imports | 5784 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 30 |
| Doc coverage | 90% (1207/1345 files) |
| Security findings | 0 |
| Estimated read cost | ~929882 tokens (chars/4, offline so $0) |
| Large files (>256KB, maybe generated) | 9: `lazyc2.py`, `lazy_loop.py`, `lazyown_mcp.py`, `mcp_generated_tools.py`, `3d-force-graph-1.73.4.min.js` (+4 more) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target LazyOwn
```

## Concept Wiki

- [modules: autonomous_daemon (172 files, cohesion 0.55)](./community_0_modules_autonomous_daemon.md)
- [cli/commands (137 files, cohesion 0.50)](./community_1_cli_commands.md)
- [modules: lazy_loop (132 files, cohesion 0.51)](./community_2_modules_lazy_loop.md)
- [cli (126 files, cohesion 0.55)](./community_3_cli.md)
- [modules: world_model (91 files, cohesion 0.43)](./community_4_modules_world_model.md)
- [modules: lazyown (80 files, cohesion 0.35)](./community_5_modules_lazyown.md)
- [modules: chain_runner (73 files, cohesion 0.53)](./community_6_modules_chain_runner.md)
- [lazyc2/security (72 files, cohesion 0.52)](./community_7_lazyc2_security.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_8_lazygui_panels.md)
- [modules: llm_budget (33 files, cohesion 0.41)](./community_9_modules_llm_budget.md)
- [modules/selection (26 files, cohesion 0.59)](./community_10_modules_selection.md)
- [modules/mediation (22 files, cohesion 0.44)](./community_11_modules_mediation.md)
- [skills/claude_md_orchestrator (13 files, cohesion 0.78)](./community_12_skills_claude_md_orchestrator.md)
- [modules: opsec_scorer (9 files, cohesion 0.50)](./community_13_modules_opsec_scorer.md)
- [modules: defense_eval (8 files, cohesion 0.64)](./community_14_modules_defense_eval.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_15_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_16_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_17_modules_polymorphic_engine.md)
- [modules/guardrails (6 files, cohesion 0.62)](./community_18_modules_guardrails.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_19_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_20_tests.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_21_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_22_modules_backdoor.md)
- [modules: lazy_netattack (2 files, cohesion 1.00)](./community_23_modules_lazy_netattack.md)
- [modules: lazy_triage (2 files, cohesion 1.00)](./community_24_modules_lazy_triage.md)
- [poc_tui (2 files, cohesion 1.00)](./community_25_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_26_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_27_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_28_tools.md)
- [orphans (245 files, cohesion 0.00)](./community_29_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 319.2 |
| `modules/lazy_loop.py` | 297.7 (large, maybe generated) |
| `utils.py` | 262.6 |
| `modules/__init__.py` | 236.0 |
| `cli/commands/_base.py` | 218.7 |

## Strongest Connections

- 3 -> 5: depends_on (strength 0.9, EXTRACTED)
- 6 -> 11: depends_on (strength 0.9, EXTRACTED)
- 6 -> 0: depends_on (strength 0.9, EXTRACTED)
- 6 -> 2: depends_on (strength 0.9, EXTRACTED)
- 6 -> 18: depends_on (strength 0.9, EXTRACTED)
- 5 -> 0: depends_on (strength 0.9, EXTRACTED)
- 1 -> 9: depends_on (strength 0.9, EXTRACTED)
- 1 -> 6: depends_on (strength 0.9, EXTRACTED)
- 1 -> 5: depends_on (strength 0.9, EXTRACTED)
- 3 -> 0: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
