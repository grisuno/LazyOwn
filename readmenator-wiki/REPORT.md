# Audit Report

*Project: LazyOwn | 2026-11-11 | offline, deterministic*

## Confidence Trail

Every edge is tagged. Extracted means parsed from source; inferred means derived heuristically; ambiguous is reported, never hidden.

| Confidence | Count | Meaning |
|------------|-------|---------|
| EXTRACTED | 6156 | Resolved import edges parsed from source |
| EXTRACTED | 14045 | Raw import statements (may include externals) |
| INFERRED | 5 | Surprising cross-community bridges |
| AMBIGUOUS | 0 | No uncertain edges are emitted by the static scanner |

## Coverage

- Files: 1566, communities: 30
- File doc coverage: 1427/1566
- Orphans (no docs at any level): 108
- Layers detected: 6
- Security findings: 0
- Large files (>256KB, maybe generated): 8 (lazyc2.py, lazy_loop.py, mcp_generated_tools.py, 3d-force-graph-1.73.4.min.js, html2pdf.bundle.min.js)

## Limits

- Python uses the ast module; all other languages use regex parsers.
- No dataflow or runtime tracing; taint follows the import graph only.
- Symbol docs come from adjacent comments; missing docs are listed, not invented.
- Centrality scores count every scanned file equally, including checked-in build artifacts; verify large files before refactoring.

## Token Benchmark

- Wiki index plus community pages estimate: ~961725 tokens (chars/4).
- Full re-read of every source file would cost strictly more on any non-trivial project; this wiki is the cheaper entry point.
- Generation cost: $0, offline, no network calls.

## Reproduce

```
readmenator . --rebuild
readmenator . wiki
```
