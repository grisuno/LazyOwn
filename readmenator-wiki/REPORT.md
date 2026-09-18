# Audit Report

*Project: LazyOwn | 2026-09-18 | offline, deterministic*

## Confidence Trail

Every edge is tagged. Extracted means parsed from source; inferred means derived heuristically; ambiguous is reported, never hidden.

| Confidence | Count | Meaning |
|------------|-------|---------|
| EXTRACTED | 3141 | Resolved import edges parsed from source |
| EXTRACTED | 7867 | Raw import statements (may include externals) |
| INFERRED | 5 | Surprising cross-community bridges |
| AMBIGUOUS | 0 | No uncertain edges are emitted by the static scanner |

## Coverage

- Files: 863, communities: 24
- File doc coverage: 735/863
- Orphans (no docs at any level): 99
- Layers detected: 6
- Security findings: 0
- Large files (>256KB, maybe generated): 7 (lazyc2.py, lazyown_mcp.py, mcp_generated_tools.py, html2pdf.bundle.min.js, vis-network-9.1.2.min.js)

## Limits

- Python uses the ast module; all other languages use regex parsers.
- No dataflow or runtime tracing; taint follows the import graph only.
- Symbol docs come from adjacent comments; missing docs are listed, not invented.
- Centrality scores count every scanned file equally, including checked-in build artifacts; verify large files before refactoring.

## Token Benchmark

- Wiki index plus community pages estimate: ~514588 tokens (chars/4).
- Full re-read of every source file would cost strictly more on any non-trivial project; this wiki is the cheaper entry point.
- Generation cost: $0, offline, no network calls.

## Reproduce

```
readmenator . --rebuild
readmenator . wiki
```
