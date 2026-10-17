# Audit Report

*Project: LazyOwn | 2026-10-17 | offline, deterministic*

## Confidence Trail

Every edge is tagged. Extracted means parsed from source; inferred means derived heuristically; ambiguous is reported, never hidden.

| Confidence | Count | Meaning |
|------------|-------|---------|
| EXTRACTED | 4517 | Resolved import edges parsed from source |
| EXTRACTED | 10408 | Raw import statements (may include externals) |
| INFERRED | 5 | Surprising cross-community bridges |
| AMBIGUOUS | 0 | No uncertain edges are emitted by the static scanner |

## Coverage

- Files: 1078, communities: 23
- File doc coverage: 949/1078
- Orphans (no docs at any level): 103
- Layers detected: 6
- Security findings: 0
- Large files (>256KB, maybe generated): 9 (lazyc2.py, lazy_loop.py, lazyown_mcp.py, mcp_generated_tools.py, 3d-force-graph-1.73.4.min.js)

## Limits

- Python uses the ast module; all other languages use regex parsers.
- No dataflow or runtime tracing; taint follows the import graph only.
- Symbol docs come from adjacent comments; missing docs are listed, not invented.
- Centrality scores count every scanned file equally, including checked-in build artifacts; verify large files before refactoring.

## Token Benchmark

- Wiki index plus community pages estimate: ~791985 tokens (chars/4).
- Full re-read of every source file would cost strictly more on any non-trivial project; this wiki is the cheaper entry point.
- Generation cost: $0, offline, no network calls.

## Reproduce

```
readmenator . --rebuild
readmenator . wiki
```
