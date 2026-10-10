# static/js

*Community 13 | 5 files | cohesion 0.44*

## Definition

This community groups 5 file(s) rooted at `static/js` with dominant language py (cohesion 0.44). Central symbols: `X`, `a`, `active_tokens`, `ae`, `but`, `e`, `h`, `i`. Core file: `static/js/jquery-3.5.1.slim.min.js` (6 symbols). Documented purpose: Centralised TUI style tokens for the LazyOwn operator surface.  This module is a thin semantic layer over :mod:`cli.themes`. It exposes a small, stable set of t.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/style.py` | py | utility | 4 | yes |
| `lazyc2/state.py` | py | utility | 0 | yes |
| `modules/search.py` | py | utility | 0 | yes |
| `static/js/jquery-3.5.1.slim.min.js` | js | utility | 6 | yes |
| `static/js/showdown-2.1.0.min.js` | js | utility | 5 | yes |

## Key Symbols

- `style` (function, `cli/style.py:49`) `def style(token, theme)` - Return the Rich style string for a semantic token.
- `active_tokens` (function, `cli/style.py:68`) `def active_tokens(payload)` - Resolve every :data:`TOKEN_KEYS` entry for the payload's theme.
- `paint` (function, `cli/style.py:84`) `def paint(text, token, payload)` - Render ``text`` with the style of ``token`` for the active theme.
- `render_prompt` (function, `cli/style.py:98`) `def render_prompt(console, segments, payload)` - Print a themed prompt line composed of ``(text, token)`` pairs.
- `e` (function, `static/js/jquery-3.5.1.slim.min.js:2`) - /*! jQuery v3.5.1 -ajax,-ajax/jsonp,-ajax/load,-ajax/script,-ajax/var/location,-ajax/var/nonce,-ajax
- `p` (function, `static/js/jquery-3.5.1.slim.min.js:2`) - /*! jQuery v3.5.1 -ajax,-ajax/jsonp,-ajax/load,-ajax/script,-ajax/var/location,-ajax/var/nonce,-ajax
- `h` (function, `static/js/jquery-3.5.1.slim.min.js:2`) - /*! jQuery v3.5.1 -ajax,-ajax/jsonp,-ajax/load,-ajax/script,-ajax/var/location,-ajax/var/nonce,-ajax
- `X` (function, `static/js/jquery-3.5.1.slim.min.js:2`) - /*! jQuery v3.5.1 -ajax,-ajax/jsonp,-ajax/load,-ajax/script,-ajax/var/location,-ajax/var/nonce,-ajax
- `ae` (function, `static/js/jquery-3.5.1.slim.min.js:2`) - /*! jQuery v3.5.1 -ajax,-ajax/jsonp,-ajax/load,-ajax/script,-ajax/var/location,-ajax/var/nonce,-ajax
- `i` (function, `static/js/jquery-3.5.1.slim.min.js:2`) - /*! jQuery v3.5.1 -ajax,-ajax/jsonp,-ajax/load,-ajax/script,-ajax/var/location,-ajax/var/nonce,-ajax
- `but` (function, `static/js/showdown-2.1.0.min.js:2`) - /*! showdown v 2.1.0 - 21-04-2022
- `must` (function, `static/js/showdown-2.1.0.min.js:2`) - /*! showdown v 2.1.0 - 21-04-2022
- `must` (function, `static/js/showdown-2.1.0.min.js:2`) - /*! showdown v 2.1.0 - 21-04-2022
- `must` (function, `static/js/showdown-2.1.0.min.js:2`) - /*! showdown v 2.1.0 - 21-04-2022
- `a` (function, `static/js/showdown-2.1.0.min.js:2`) - /*! showdown v 2.1.0 - 21-04-2022

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 16
- Cross-boundary resolved imports (EXTRACTED): 8

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.44?

## Sources

- `cli/style.py`
- `lazyc2/state.py`
- `modules/search.py`
- `static/js/jquery-3.5.1.slim.min.js`
- `static/js/showdown-2.1.0.min.js`
