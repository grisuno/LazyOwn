# Second Brain

*Last synthesized: 2026-10-10 | 944 files | 23 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `_base.py`. Architecturally it is 6 layers, dominant utility (592 files) across 23 import-based communities. Recorded risk surface: 0 security findings and 21 dependency cycles.

Surprising tissue lives between cli/commands, modules: autonomous_daemon, modules: lazyc2: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (86% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 944 |
| Symbols | 18242 |
| Resolved imports | 3526 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 23 |
| Doc coverage | 86% (814/944 files) |
| Security findings | 0 |
| Estimated read cost | ~717020 tokens (chars/4, offline so $0) |
| Large files (>256KB, maybe generated) | 8: `lazyc2.py`, `lazyown_mcp.py`, `mcp_generated_tools.py`, `3d-force-graph-1.73.4.min.js`, `html2pdf.bundle.min.js` (+3 more) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target LazyOwn
```

## Concept Wiki

- [cli/commands (161 files, cohesion 0.62)](./community_0_cli_commands.md)
- [modules: autonomous_daemon (114 files, cohesion 0.58)](./community_1_modules_autonomous_daemon.md)
- [modules: lazyc2 (89 files, cohesion 0.46)](./community_2_modules_lazyc2.md)
- [cli (85 files, cohesion 0.54)](./community_3_cli.md)
- [modules: quill-2.0.3 (75 files, cohesion 0.48)](./community_4_modules_quill_2_0_3.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_5_lazygui_panels.md)
- [modules: world_model (37 files, cohesion 0.42)](./community_6_modules_world_model.md)
- [skills/claude_md_orchestrator (28 files, cohesion 0.75)](./community_7_skills_claude_md_orchestrator.md)
- [lazyc2/blueprints (26 files, cohesion 0.49)](./community_8_lazyc2_blueprints.md)
- [modules: lazy_loop (20 files, cohesion 0.49)](./community_9_modules_lazy_loop.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_10_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_11_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_12_modules_polymorphic_engine.md)
- [static/js (5 files, cohesion 0.44)](./community_13_static_js.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_14_contrib_legacy.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_15_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_16_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_17_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_18_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_19_scripts_migrate_lazyown.md)
- [test (2 files, cohesion 1.00)](./community_20_test.md)
- [tools (2 files, cohesion 1.00)](./community_21_tools.md)
- [orphans (210 files, cohesion 0.00)](./community_22_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 247.2 |
| `utils.py` | 198.1 |
| `cli/commands/_base.py` | 176.7 |
| `skills/lazyown_mcp.py` | 165.0 (large, maybe generated) |
| `lazyc2.py` | 117.1 (large, maybe generated) |

## Strongest Connections

- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 0 -> 4: depends_on (strength 0.9, EXTRACTED)
- 2 -> 0: depends_on (strength 0.9, EXTRACTED)
- 2 -> 8: depends_on (strength 0.9, EXTRACTED)
- 0 -> 8: depends_on (strength 0.9, EXTRACTED)
- 3 -> 2: depends_on (strength 0.9, EXTRACTED)
- 4 -> 3: depends_on (strength 0.9, EXTRACTED)
- 10 -> 0: depends_on (strength 0.9, EXTRACTED)
- 4 -> 6: depends_on (strength 0.9, EXTRACTED)
- 4 -> 1: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
