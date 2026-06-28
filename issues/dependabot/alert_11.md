# Dependabot Alert #11: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2025-62707
- **Created:** 2026-06-07T17:50:21Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/11

## Summary
pypdf possibly loops infinitely when reading DCT inline images without EOF marker

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to an infinite loop. This requires parsing the content stream of a page which has an inline image using the DCTDecode filter.

### Patches
This has been fixed in [pypdf==6.1.3](https://github.com/py-pdf/pypdf/releases/tag/6.1.3).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3501](https://github.com/py-pdf/pypdf/pull/3501).
