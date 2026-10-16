# Second Brain

*Last synthesized: 2026-10-15 | 1037 files | 23 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `lazyown_mcp.py`. Architecturally it is 6 layers, dominant utility (630 files) across 23 import-based communities. Recorded risk surface: 0 security findings and 56 dependency cycles.

Surprising tissue lives between cli/commands, modules: lazyc2, cli: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (88% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1037 |
| Symbols | 19990 |
| Resolved imports | 4363 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 23 |
| Doc coverage | 88% (909/1037 files) |
| Security findings | 0 |
| Estimated read cost | ~777342 tokens (chars/4, offline so $0) |
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

- [cli/commands (157 files, cohesion 0.55)](./community_0_cli_commands.md)
- [modules: lazyc2 (128 files, cohesion 0.52)](./community_1_modules_lazyc2.md)
- [cli (113 files, cohesion 0.56)](./community_2_cli.md)
- [modules: autonomous_daemon (108 files, cohesion 0.51)](./community_3_modules_autonomous_daemon.md)
- [modules: lazy_loop (67 files, cohesion 0.61)](./community_4_modules_lazy_loop.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_5_lazygui_panels.md)
- [skills/claude_md_orchestrator (37 files, cohesion 0.69)](./community_6_skills_claude_md_orchestrator.md)
- [static/js (28 files, cohesion 0.45)](./community_7_static_js.md)
- [modules: llm_budget (26 files, cohesion 0.43)](./community_8_modules_llm_budget.md)
- [modules: atomic_exploit_bridge (23 files, cohesion 0.33)](./community_9_modules_atomic_exploit_bridge.md)
- [modules: opsec_scorer (20 files, cohesion 0.37)](./community_10_modules_opsec_scorer.md)
- [modules: finding_lifecycle (12 files, cohesion 0.50)](./community_11_modules_finding_lifecycle.md)
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
- [orphans (226 files, cohesion 0.00)](./community_22_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 267.2 |
| `utils.py` | 216.4 |
| `skills/lazyown_mcp.py` | 194.2 (large, maybe generated) |
| `cli/commands/_base.py` | 184.7 |
| `modules/lazy_loop.py` | 175.6 (large, maybe generated) |

## Strongest Connections

- 2 -> 0: depends_on (strength 0.9, EXTRACTED)
- 10 -> 1: depends_on (strength 0.9, EXTRACTED)
- 10 -> 0: depends_on (strength 0.9, EXTRACTED)
- 0 -> 8: depends_on (strength 0.9, EXTRACTED)
- 0 -> 9: depends_on (strength 0.9, EXTRACTED)
- 2 -> 1: depends_on (strength 0.9, EXTRACTED)
- 12 -> 0: depends_on (strength 0.9, EXTRACTED)
- 8 -> 3: depends_on (strength 0.9, EXTRACTED)
- 1 -> 0: depends_on (strength 0.9, EXTRACTED)
- 3 -> 0: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
