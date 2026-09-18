# Second Brain

*Last synthesized: 2026-09-18 | 863 files | 24 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `_base.py`. Architecturally it is 6 layers, dominant utility (467 files) across 24 import-based communities. Recorded risk surface: 0 security findings and 26 dependency cycles.

Surprising tissue lives between cli/commands (community 0), tests (community 1), cli/commands (community 2): 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (85% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 863 |
| Symbols | 16739 |
| Resolved imports | 3141 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 24 |
| Doc coverage | 85% (735/863 files) |
| Security findings | 0 |
| Estimated read cost | ~515188 tokens (chars/4, offline so $0) |
| Large files (>256KB, maybe generated) | 7: `lazyc2.py`, `lazyown_mcp.py`, `mcp_generated_tools.py`, `html2pdf.bundle.min.js`, `vis-network-9.1.2.min.js` (+2 more) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target LazyOwn
```

## Concept Wiki

- [cli/commands (community 0) (122 files, cohesion 0.62)](./community_0_cli_commands.md)
- [tests (community 1) (215 files, cohesion 0.68)](./community_1_tests.md)
- [cli/commands (community 2) (3 files, cohesion 0.50)](./community_2_cli_commands.md)
- [modules (community 3) (7 files, cohesion 0.88)](./community_3_modules.md)
- [modules (community 4) (180 files, cohesion 0.70)](./community_4_modules.md)
- [modules (community 5) (6 files, cohesion 0.83)](./community_5_modules.md)
- [modules (community 6) (17 files, cohesion 0.41)](./community_6_modules.md)
- [lazyc2/security (11 files, cohesion 0.63)](./community_7_lazyc2_security.md)
- [tests (community 8) (3 files, cohesion 0.50)](./community_8_tests.md)
- [tests (community 9) (4 files, cohesion 0.75)](./community_9_tests.md)
- [lazygui/panels (43 files, cohesion 0.91)](./community_10_lazygui_panels.md)
- [lazygui/theme/palettes (7 files, cohesion 0.55)](./community_11_lazygui_theme_palettes.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_12_modules_backdoor.md)
- [modules/legacy (5 files, cohesion 0.80)](./community_13_modules_legacy.md)
- [poc_tui (community 14) (4 files, cohesion 0.60)](./community_14_poc_tui.md)
- [poc_tui (community 15) (2 files, cohesion 1.00)](./community_15_poc_tui.md)
- [scripts (community 16) (2 files, cohesion 1.00)](./community_16_scripts.md)
- [scripts (community 17) (3 files, cohesion 1.00)](./community_17_scripts.md)
- [scripts (community 18) (2 files, cohesion 1.00)](./community_18_scripts.md)
- [skills/claude_md_orchestrator (13 files, cohesion 0.85)](./community_19_skills_claude_md_orchestrator.md)
- [skills/hermes-lazyown (7 files, cohesion 0.85)](./community_20_skills_hermes_lazyown.md)
- [test (2 files, cohesion 1.00)](./community_21_test.md)
- [tools (2 files, cohesion 1.00)](./community_22_tools.md)
- [orphans (201 files, cohesion 0.00)](./community_23_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 245.2 |
| `utils.py` | 186.2 |
| `cli/commands/_base.py` | 166.7 |
| `skills/lazyown_mcp.py` | 146.1 (large, maybe generated) |
| `lazyown.py` | 120.3 |

## Strongest Connections

- 1 -> 0: depends_on (strength 0.9, EXTRACTED)
- 1 -> 4: depends_on (strength 0.9, EXTRACTED)
- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 0 -> 4: depends_on (strength 0.9, EXTRACTED)
- 2 -> 0: depends_on (strength 0.9, EXTRACTED)
- 0 -> 6: depends_on (strength 0.9, EXTRACTED)
- 5 -> 0: depends_on (strength 0.9, EXTRACTED)
- 6 -> 1: depends_on (strength 0.9, EXTRACTED)
- 7 -> 4: depends_on (strength 0.9, EXTRACTED)
- 8 -> 1: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
