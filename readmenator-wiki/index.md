# Second Brain

*Last synthesized: 2026-11-13 | 1627 files | 30 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `_context.py`, `lazy_loop.py`, `logging.py`. Architecturally it is 6 layers, dominant utility (983 files) across 30 import-based communities. Recorded risk surface: 0 security findings and 156 dependency cycles.

Surprising tissue lives between skills/mcp_tools, modules: lazy_loop, cli/commands: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (91% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1627 |
| Symbols | 25636 |
| Resolved imports | 6418 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 30 |
| Doc coverage | 91% (1486/1627 files) |
| Security findings | 0 |
| Estimated read cost | ~996079 tokens (chars/4, offline so $0) |
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

- [skills/mcp_tools (206 files, cohesion 0.63)](./community_0_skills_mcp_tools.md)
- [modules: lazy_loop (166 files, cohesion 0.54)](./community_1_modules_lazy_loop.md)
- [cli/commands (139 files, cohesion 0.45)](./community_2_cli_commands.md)
- [modules: lazyown (139 files, cohesion 0.38)](./community_3_modules_lazyown.md)
- [modules: lazyc2 (135 files, cohesion 0.46)](./community_4_modules_lazyc2.md)
- [cli (123 files, cohesion 0.55)](./community_5_cli.md)
- [modules: world_model (99 files, cohesion 0.43)](./community_6_modules_world_model.md)
- [modules: lazyown_facts (63 files, cohesion 0.54)](./community_7_modules_lazyown_facts.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_8_lazygui_panels.md)
- [static/js (43 files, cohesion 0.48)](./community_9_static_js.md)
- [modules: llm_budget (43 files, cohesion 0.43)](./community_10_modules_llm_budget.md)
- [modules: bof_registry (43 files, cohesion 0.46)](./community_11_modules_bof_registry.md)
- [modules/selection (37 files, cohesion 0.66)](./community_12_modules_selection.md)
- [skills/claude_md_orchestrator (30 files, cohesion 0.68)](./community_13_skills_claude_md_orchestrator.md)
- [modules: defense_eval (8 files, cohesion 0.64)](./community_14_modules_defense_eval.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_15_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_16_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_17_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_18_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_19_tests.md)
- [modules: memory_store (3 files, cohesion 1.00)](./community_20_modules_memory_store.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_21_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_22_modules_backdoor.md)
- [modules: lazy_netattack (2 files, cohesion 1.00)](./community_23_modules_lazy_netattack.md)
- [modules: lazy_triage (2 files, cohesion 1.00)](./community_24_modules_lazy_triage.md)
- [poc_tui (2 files, cohesion 1.00)](./community_25_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_26_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_27_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_28_tools.md)
- [orphans (250 files, cohesion 0.00)](./community_29_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `skills/mcp_tools/_context.py` | 380.1 |
| `modules/lazy_loop.py` | 348.1 (large, maybe generated) |
| `core/logging.py` | 335.2 |
| `modules/__init__.py` | 298.0 |
| `utils.py` | 270.7 |

## Strongest Connections

- 5 -> 3: depends_on (strength 0.9, EXTRACTED)
- 7 -> 1: depends_on (strength 0.9, EXTRACTED)
- 7 -> 0: depends_on (strength 0.9, EXTRACTED)
- 7 -> 2: depends_on (strength 0.9, EXTRACTED)
- 7 -> 11: depends_on (strength 0.9, EXTRACTED)
- 3 -> 4: depends_on (strength 0.9, EXTRACTED)
- 2 -> 10: depends_on (strength 0.9, EXTRACTED)
- 2 -> 3: depends_on (strength 0.9, EXTRACTED)
- 5 -> 4: depends_on (strength 0.9, EXTRACTED)
- 6 -> 5: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
