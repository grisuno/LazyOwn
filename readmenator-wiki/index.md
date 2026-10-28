# Second Brain

*Last synthesized: 2026-10-28 | 1216 files | 24 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `lazy_loop.py`. Architecturally it is 6 layers, dominant utility (714 files) across 24 import-based communities. Recorded risk surface: 0 security findings and 113 dependency cycles.

Surprising tissue lives between cli/commands, modules: lazyown_mcp, modules: lazy_loop: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (90% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1216 |
| Symbols | 22854 |
| Resolved imports | 5263 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 24 |
| Doc coverage | 90% (1090/1216 files) |
| Security findings | 0 |
| Estimated read cost | ~873241 tokens (chars/4, offline so $0) |
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

- [cli/commands (166 files, cohesion 0.53)](./community_0_cli_commands.md)
- [modules: lazyown_mcp (166 files, cohesion 0.54)](./community_1_modules_lazyown_mcp.md)
- [modules: lazy_loop (119 files, cohesion 0.55)](./community_2_modules_lazy_loop.md)
- [cli (95 files, cohesion 0.50)](./community_3_cli.md)
- [modules: world_model (91 files, cohesion 0.44)](./community_4_modules_world_model.md)
- [static/js (64 files, cohesion 0.40)](./community_5_static_js.md)
- [lazyc2/security (59 files, cohesion 0.47)](./community_6_lazyc2_security.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_7_lazygui_panels.md)
- [modules: chain_runner (44 files, cohesion 0.53)](./community_8_modules_chain_runner.md)
- [modules: llm_budget (44 files, cohesion 0.44)](./community_9_modules_llm_budget.md)
- [skills/claude_md_orchestrator (23 files, cohesion 0.73)](./community_10_skills_claude_md_orchestrator.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_11_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_12_modules_saas_attacks.md)
- [skills/hermes-lazyown (7 files, cohesion 0.85)](./community_13_skills_hermes_lazyown.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_14_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_15_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_16_tests.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_17_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_18_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_19_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_20_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_21_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_22_tools.md)
- [orphans (242 files, cohesion 0.00)](./community_23_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 317.2 |
| `utils.py` | 244.6 |
| `modules/lazy_loop.py` | 236.7 (large, maybe generated) |
| `skills/lazyown_mcp.py` | 203.5 (large, maybe generated) |
| `cli/commands/_base.py` | 200.7 |

## Strongest Connections

- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 0 -> 5: depends_on (strength 0.9, EXTRACTED)
- 8 -> 2: depends_on (strength 0.9, EXTRACTED)
- 8 -> 1: depends_on (strength 0.9, EXTRACTED)
- 8 -> 9: depends_on (strength 0.9, EXTRACTED)
- 3 -> 1: depends_on (strength 0.9, EXTRACTED)
- 0 -> 9: depends_on (strength 0.9, EXTRACTED)
- 3 -> 4: depends_on (strength 0.9, EXTRACTED)
- 3 -> 2: depends_on (strength 0.9, EXTRACTED)
- 11 -> 0: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
