# tools

*Community 22 | 2 files | cohesion 1.00*

## Definition

This community groups 2 file(s) rooted at `tools` with dominant language py (cohesion 1.00). Central symbols: `font`, `main`, `render`. Core file: `tools/gen_demo_gifs.py` (3 symbols). Documented purpose: Generate LazyOwn demo GIFs without external services..

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tools/gen_demo_gifs.py` | py | utility | 3 | yes |
| `tools/gen_demo_gifs_extra.py` | py | utility | 1 | yes |

## Key Symbols

- `font` (function, `tools/gen_demo_gifs.py:12`) `def font(size)` - Resolve a monospace font with stdlib fallback.
- `render` (function, `tools/gen_demo_gifs.py:20`) `def render(lines, path, hold)` - Render terminal line-by-line frames.
- `main` (function, `tools/gen_demo_gifs.py:68`) `def main()` - Render the three core GIFs.
- `main` (function, `tools/gen_demo_gifs_extra.py:47`) `def main()` - Render the four extended GIFs.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 1
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in tools changed?
- Should tools be split, given cohesion 1.00?

## Sources

- `tools/gen_demo_gifs.py`
- `tools/gen_demo_gifs_extra.py`
