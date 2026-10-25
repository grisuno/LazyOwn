# Second Brain

*Last synthesized: 2026-10-25 | 1183 files | 26 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `lazy_loop.py`. Architecturally it is 6 layers, dominant utility (701 files) across 26 import-based communities. Recorded risk surface: 0 security findings and 136 dependency cycles.

Surprising tissue lives between modules: autonomous_daemon, cli/commands, cli: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (89% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1183 |
| Symbols | 22078 |
| Resolved imports | 5046 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 26 |
| Doc coverage | 89% (1054/1183 files) |
| Security findings | 0 |
| Estimated read cost | ~844205 tokens (chars/4, offline so $0) |
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

- [modules: autonomous_daemon (184 files, cohesion 0.57)](./community_0_modules_autonomous_daemon.md)
- [cli/commands (160 files, cohesion 0.53)](./community_1_cli_commands.md)
- [cli (126 files, cohesion 0.55)](./community_2_cli.md)
- [modules: lazy_loop (122 files, cohesion 0.58)](./community_3_modules_lazy_loop.md)
- [modules: world_model (62 files, cohesion 0.41)](./community_4_modules_world_model.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_5_lazygui_panels.md)
- [lazyc2/security (52 files, cohesion 0.47)](./community_6_lazyc2_security.md)
- [modules: lazyown_facts (38 files, cohesion 0.53)](./community_7_modules_lazyown_facts.md)
- [static/js (29 files, cohesion 0.41)](./community_8_static_js.md)
- [skills/claude_md_orchestrator (23 files, cohesion 0.73)](./community_9_skills_claude_md_orchestrator.md)
- [core (22 files, cohesion 0.43)](./community_10_core.md)
- [modules: opsec_scorer (14 files, cohesion 0.43)](./community_11_modules_opsec_scorer.md)
- [modules: defense_eval (8 files, cohesion 0.64)](./community_12_modules_defense_eval.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_13_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_14_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_15_modules_polymorphic_engine.md)
- [modules/guardrails (6 files, cohesion 0.67)](./community_16_modules_guardrails.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_17_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_18_tests.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_19_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_20_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_21_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_22_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_23_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_24_tools.md)
- [orphans (241 files, cohesion 0.00)](./community_25_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 309.2 |
| `utils.py` | 232.5 |
| `modules/lazy_loop.py` | 228.1 (large, maybe generated) |
| `skills/lazyown_mcp.py` | 202.6 (large, maybe generated) |
| `cli/commands/_base.py` | 194.7 |

## Strongest Connections

- 2 -> 1: depends_on (strength 0.9, EXTRACTED)
- 1 -> 3: depends_on (strength 0.9, EXTRACTED)
- 7 -> 3: depends_on (strength 0.9, EXTRACTED)
- 7 -> 0: depends_on (strength 0.9, EXTRACTED)
- 7 -> 16: depends_on (strength 0.9, EXTRACTED)
- 8 -> 3: depends_on (strength 0.9, EXTRACTED)
- 2 -> 0: depends_on (strength 0.9, EXTRACTED)
- 1 -> 10: depends_on (strength 0.9, EXTRACTED)
- 2 -> 3: depends_on (strength 0.9, EXTRACTED)
- 13 -> 1: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
