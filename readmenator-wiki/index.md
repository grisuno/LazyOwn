# Second Brain

*Last synthesized: 2026-10-18 | 1098 files | 23 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `lazyown_mcp.py`. Architecturally it is 6 layers, dominant utility (658 files) across 23 import-based communities. Recorded risk surface: 0 security findings and 73 dependency cycles.

Surprising tissue lives between cli/commands, modules: lazyc2, modules: autonomous_daemon: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (88% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1098 |
| Symbols | 20729 |
| Resolved imports | 4579 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 23 |
| Doc coverage | 88% (969/1098 files) |
| Security findings | 0 |
| Estimated read cost | ~800871 tokens (chars/4, offline so $0) |
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

- [cli/commands (162 files, cohesion 0.54)](./community_0_cli_commands.md)
- [modules: lazyc2 (141 files, cohesion 0.51)](./community_1_modules_lazyc2.md)
- [modules: autonomous_daemon (115 files, cohesion 0.51)](./community_2_modules_autonomous_daemon.md)
- [cli (112 files, cohesion 0.54)](./community_3_cli.md)
- [modules: lazy_loop (99 files, cohesion 0.57)](./community_4_modules_lazy_loop.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_5_lazygui_panels.md)
- [modules: llm_budget (35 files, cohesion 0.43)](./community_6_modules_llm_budget.md)
- [static/js (31 files, cohesion 0.51)](./community_7_static_js.md)
- [skills/claude_md_orchestrator (29 files, cohesion 0.70)](./community_8_skills_claude_md_orchestrator.md)
- [modules: lazyown_facts (22 files, cohesion 0.46)](./community_9_modules_lazyown_facts.md)
- [modules: surface_graph (15 files, cohesion 0.50)](./community_10_modules_surface_graph.md)
- [modules: opsec_scorer (9 files, cohesion 0.53)](./community_11_modules_opsec_scorer.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_12_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_13_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_14_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_15_contrib_legacy.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_16_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_17_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_18_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_19_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_20_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_21_tools.md)
- [orphans (236 files, cohesion 0.00)](./community_22_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 279.2 |
| `utils.py` | 216.4 |
| `skills/lazyown_mcp.py` | 200.6 (large, maybe generated) |
| `modules/lazy_loop.py` | 192.1 (large, maybe generated) |
| `cli/commands/_base.py` | 184.7 |

## Strongest Connections

- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 9 -> 2: depends_on (strength 0.9, EXTRACTED)
- 7 -> 6: depends_on (strength 0.9, EXTRACTED)
- 3 -> 1: depends_on (strength 0.9, EXTRACTED)
- 0 -> 6: depends_on (strength 0.9, EXTRACTED)
- 0 -> 1: depends_on (strength 0.9, EXTRACTED)
- 3 -> 4: depends_on (strength 0.9, EXTRACTED)
- 12 -> 0: depends_on (strength 0.9, EXTRACTED)
- 6 -> 3: depends_on (strength 0.9, EXTRACTED)
- 6 -> 2: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
