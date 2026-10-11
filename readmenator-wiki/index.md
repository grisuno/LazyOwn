# Second Brain

*Last synthesized: 2026-10-11 | 961 files | 26 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `_base.py`. Architecturally it is 6 layers, dominant utility (595 files) across 26 import-based communities. Recorded risk surface: 0 security findings and 21 dependency cycles.

Surprising tissue lives between cli/commands, modules: autonomous_daemon, modules: lazyown: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (86% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 961 |
| Symbols | 18387 |
| Resolved imports | 3563 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 26 |
| Doc coverage | 86% (831/961 files) |
| Security findings | 0 |
| Estimated read cost | ~720946 tokens (chars/4, offline so $0) |
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

- [cli/commands (118 files, cohesion 0.56)](./community_0_cli_commands.md)
- [modules: autonomous_daemon (115 files, cohesion 0.57)](./community_1_modules_autonomous_daemon.md)
- [modules: lazyown (70 files, cohesion 0.36)](./community_2_modules_lazyown.md)
- [modules: lazy_sentinel4 (64 files, cohesion 0.45)](./community_3_modules_lazy_sentinel4.md)
- [cli: status_bar (61 files, cohesion 0.51)](./community_4_cli_status_bar.md)
- [static/js (55 files, cohesion 0.42)](./community_5_static_js.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_6_lazygui_panels.md)
- [lazyc2/security (53 files, cohesion 0.55)](./community_7_lazyc2_security.md)
- [modules: dashboard_tui (38 files, cohesion 0.47)](./community_8_modules_dashboard_tui.md)
- [modules: lazy_loop (25 files, cohesion 0.51)](./community_9_modules_lazy_loop.md)
- [cli: banner_config (19 files, cohesion 0.41)](./community_10_cli_banner_config.md)
- [skills/claude_md_orchestrator (19 files, cohesion 0.80)](./community_11_skills_claude_md_orchestrator.md)
- [cli: exploration (9 files, cohesion 0.50)](./community_12_cli_exploration.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_13_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_14_modules_saas_attacks.md)
- [modules: network_opsec (6 files, cohesion 0.71)](./community_15_modules_network_opsec.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_16_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_17_contrib_legacy.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_18_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_19_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_20_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_21_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_22_scripts_migrate_lazyown.md)
- [test (2 files, cohesion 1.00)](./community_23_test.md)
- [tools (2 files, cohesion 1.00)](./community_24_tools.md)
- [orphans (215 files, cohesion 0.00)](./community_25_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 247.2 |
| `utils.py` | 202.1 |
| `cli/commands/_base.py` | 180.7 |
| `skills/lazyown_mcp.py` | 168.5 (large, maybe generated) |
| `lazyc2.py` | 117.7 (large, maybe generated) |

## Strongest Connections

- 4 -> 0: depends_on (strength 0.9, EXTRACTED)
- 0 -> 5: depends_on (strength 0.9, EXTRACTED)
- 2 -> 10: depends_on (strength 0.9, EXTRACTED)
- 10 -> 3: depends_on (strength 0.9, EXTRACTED)
- 4 -> 2: depends_on (strength 0.9, EXTRACTED)
- 12 -> 4: depends_on (strength 0.9, EXTRACTED)
- 3 -> 4: depends_on (strength 0.9, EXTRACTED)
- 13 -> 0: depends_on (strength 0.9, EXTRACTED)
- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 3 -> 8: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
