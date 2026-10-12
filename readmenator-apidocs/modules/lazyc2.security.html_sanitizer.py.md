# `lazyc2.security.html_sanitizer`

> Source: [lazyc2/security/html_sanitizer.py:1](../../lazyc2/security/html_sanitizer.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

HTML sanitizer backed by ``bleach`` for the LazyOwn C2 web layer.

Contract: this module is the single source of truth for cleaning
operator-supplied HTML before it is rendered. It replaces the previous
regex-based approach in [`lazyc2`](lazyc2.__init__.py.md), which was vulnerable to nested
tag and ``javascript:`` URI bypasses.

Invariants:

1. ``<script>``, ``<iframe>``, ``<object>``, ``<embed>``, ``<style>`` and
   their contents are removed entirely.
2. ``on*`` event handlers are stripped from every element.
3. ``javascript:`` URIs in ``href`` and ``src`` are neutralised.
4. Benign tags (``p``, ``strong``, ``em``, ``ul``, ``ol``, ``li``, `[`a`](static.js.xterm-addon-web-links-0.5.0.js.md#a)`,
   ``code``, ``pre``, ``h1``..``h6``, ``blockquote``) survive untouched.
5. The allowlist can be overridden by the caller, in which case the
   defaults from [`lazyc2.security.constants`](lazyc2.security.constants.py.md) are not used.

Config keys owned: none (the defaults live in
[`lazyc2.security.constants`](lazyc2.security.constants.py.md)).

## Contents

- **Functions:** [`sanitize_html`](#sanitize_html)

## Functions

<a id="sanitize_html"></a>

### `sanitize_html`

`function` | [lazyc2/security/html_sanitizer.py:78](../../lazyc2/security/html_sanitizer.py#L78)

```python
def sanitize_html(raw_html: str | None, allowed_tags: Iterable[str] | None = None, allowed_attributes: dict[str, Iterable[str]] | None = None) -> str
```

Return a sanitized HTML string safe for ``render_template``.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `raw_html` | `str \| None` |  | The HTML to clean. ``None`` or empty returns ``""``. |
| `allowed_tags` | `Iterable[str] \| None` | `None` | Optional override for the tag allowlist. |
| `allowed_attributes` | `dict[str, Iterable[str]] \| None` | `None` | Optional override for the attribute map. |

**Returns:** `str` - The sanitized HTML. Guaranteed to contain no ``<script>``,
``<iframe>``, ``<object>``, ``<embed>``, ``<style>``, ``on*``
attributes, ``javascript:`` URIs, or HTML comments.

---
