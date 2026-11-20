# Second Brain

*Last synthesized: 2026-11-19 | 1700 files | 28 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `lazy_loop.py`, `_context.py`, `logging.py`. Architecturally it is 6 layers, dominant utility (1012 files) across 28 import-based communities. Recorded risk surface: 0 security findings and 172 dependency cycles.

Surprising tissue lives between skills/mcp_tools, modules: lazyc2, modules: lazy_loop: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (92% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1700 |
| Symbols | 26546 |
| Resolved imports | 6765 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 28 |
| Doc coverage | 92% (1561/1700 files) |
| Security findings | 0 |
| Estimated read cost | ~1033101 tokens (chars/4, offline so $0) |
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

- [skills/mcp_tools (226 files, cohesion 0.62)](./community_0_skills_mcp_tools.md)
- [modules: lazyc2 (176 files, cohesion 0.49)](./community_1_modules_lazyc2.md)
- [modules: lazy_loop (162 files, cohesion 0.52)](./community_2_modules_lazy_loop.md)
- [cli/commands (158 files, cohesion 0.47)](./community_3_cli_commands.md)
- [modules: lazyown (151 files, cohesion 0.41)](./community_4_modules_lazyown.md)
- [modules: lazyown_facts (110 files, cohesion 0.58)](./community_5_modules_lazyown_facts.md)
- [modules: autonomous_exploit_engine (87 files, cohesion 0.46)](./community_6_modules_autonomous_exploit_engine.md)
- [modules: world_model (84 files, cohesion 0.42)](./community_7_modules_world_model.md)
- [cli (68 files, cohesion 0.49)](./community_8_cli.md)
- [static/js (62 files, cohesion 0.46)](./community_9_static_js.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_10_lazygui_panels.md)
- [modules: llm_budget (43 files, cohesion 0.42)](./community_11_modules_llm_budget.md)
- [skills/claude_md_orchestrator (14 files, cohesion 0.79)](./community_12_skills_claude_md_orchestrator.md)
- [modules: defense_eval (8 files, cohesion 0.64)](./community_13_modules_defense_eval.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_14_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_15_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_16_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_17_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_18_tests.md)
- [modules: memory_store (3 files, cohesion 1.00)](./community_19_modules_memory_store.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_20_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_21_modules_backdoor.md)
- [modules: lazy_netattack (2 files, cohesion 1.00)](./community_22_modules_lazy_netattack.md)
- [modules: lazy_triage (2 files, cohesion 1.00)](./community_23_modules_lazy_triage.md)
- [poc_tui (2 files, cohesion 1.00)](./community_24_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_25_scripts_check_contract_manifest.md)
- [tools (2 files, cohesion 1.00)](./community_26_tools.md)
- [orphans (250 files, cohesion 0.00)](./community_27_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `modules/lazy_loop.py` | 401.0 (large, maybe generated) |
| `skills/mcp_tools/_context.py` | 386.1 |
| `core/logging.py` | 349.2 |
| `modules/__init__.py` | 330.0 |
| `utils.py` | 278.7 |

## Strongest Connections

- 8 -> 4: depends_on (strength 0.9, EXTRACTED)
- 8 -> 3: depends_on (strength 0.9, EXTRACTED)
- 5 -> 2: depends_on (strength 0.9, EXTRACTED)
- 5 -> 0: depends_on (strength 0.9, EXTRACTED)
- 5 -> 3: depends_on (strength 0.9, EXTRACTED)
- 5 -> 1: depends_on (strength 0.9, EXTRACTED)
- 9 -> 4: depends_on (strength 0.9, EXTRACTED)
- 4 -> 1: depends_on (strength 0.9, EXTRACTED)
- 3 -> 4: depends_on (strength 0.9, EXTRACTED)
- 3 -> 9: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
