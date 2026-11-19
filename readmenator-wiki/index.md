# Second Brain

*Last synthesized: 2026-11-19 | 1671 files | 27 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `_context.py`, `lazy_loop.py`, `logging.py`. Architecturally it is 6 layers, dominant utility (1000 files) across 27 import-based communities. Recorded risk surface: 0 security findings and 167 dependency cycles.

Surprising tissue lives between skills/mcp_tools, modules: lazyc2, cli/commands: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (92% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1671 |
| Symbols | 26215 |
| Resolved imports | 6625 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 27 |
| Doc coverage | 92% (1532/1671 files) |
| Security findings | 0 |
| Estimated read cost | ~1022261 tokens (chars/4, offline so $0) |
| Large files (>256KB, maybe generated) | 8: `lazyc2.py`, `lazy_loop.py`, `mcp_generated_tools.py`, `3d-force-graph-1.73.4.min.js`, `html2pdf.bundle.min.js` (+3 more) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target LazyOwn
```

## Concept Wiki

- [skills/mcp_tools (214 files, cohesion 0.62)](./community_0_skills_mcp_tools.md)
- [modules: lazyc2 (173 files, cohesion 0.49)](./community_1_modules_lazyc2.md)
- [cli/commands (152 files, cohesion 0.46)](./community_2_cli_commands.md)
- [modules: lazy_loop (152 files, cohesion 0.51)](./community_3_modules_lazy_loop.md)
- [cli (148 files, cohesion 0.58)](./community_4_cli.md)
- [modules: world_model (122 files, cohesion 0.45)](./community_5_modules_world_model.md)
- [modules: lazyown (119 files, cohesion 0.38)](./community_6_modules_lazyown.md)
- [modules: lazyown_facts (116 files, cohesion 0.50)](./community_7_modules_lazyown_facts.md)
- [modules: llm_budget (54 files, cohesion 0.44)](./community_8_modules_llm_budget.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_9_lazygui_panels.md)
- [modules/selection (40 files, cohesion 0.57)](./community_10_modules_selection.md)
- [skills/hermes-lazyown (14 files, cohesion 0.56)](./community_11_skills_hermes_lazyown.md)
- [skills/claude_md_orchestrator (13 files, cohesion 0.78)](./community_12_skills_claude_md_orchestrator.md)
- [modules: defense_eval (8 files, cohesion 0.64)](./community_13_modules_defense_eval.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_14_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_15_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_16_modules_polymorphic_engine.md)
- [tests (4 files, cohesion 1.00)](./community_17_tests.md)
- [modules: memory_store (3 files, cohesion 1.00)](./community_18_modules_memory_store.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_19_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_20_modules_backdoor.md)
- [modules: lazy_netattack (2 files, cohesion 1.00)](./community_21_modules_lazy_netattack.md)
- [modules: lazy_triage (2 files, cohesion 1.00)](./community_22_modules_lazy_triage.md)
- [poc_tui (2 files, cohesion 1.00)](./community_23_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_24_scripts_check_contract_manifest.md)
- [tools (2 files, cohesion 1.00)](./community_25_tools.md)
- [orphans (250 files, cohesion 0.00)](./community_26_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `skills/mcp_tools/_context.py` | 386.1 |
| `modules/lazy_loop.py` | 367.2 (large, maybe generated) |
| `core/logging.py` | 347.2 |
| `modules/__init__.py` | 312.0 |
| `utils.py` | 276.7 |

## Strongest Connections

- 4 -> 6: depends_on (strength 0.9, EXTRACTED)
- 7 -> 10: depends_on (strength 0.9, EXTRACTED)
- 7 -> 3: depends_on (strength 0.9, EXTRACTED)
- 7 -> 0: depends_on (strength 0.9, EXTRACTED)
- 7 -> 2: depends_on (strength 0.9, EXTRACTED)
- 7 -> 1: depends_on (strength 0.9, EXTRACTED)
- 6 -> 1: depends_on (strength 0.9, EXTRACTED)
- 2 -> 8: depends_on (strength 0.9, EXTRACTED)
- 2 -> 6: depends_on (strength 0.9, EXTRACTED)
- 4 -> 1: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
