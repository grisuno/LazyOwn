# Dependabot Alert #12: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2025-62708
- **Created:** 2026-06-07T17:50:21Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/12

## Summary
pypdf can exhaust RAM via manipulated LZWDecode streams

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to large memory usage. This requires parsing the content stream of a page using the LZWDecode filter.

### Patches
This has been fixed in [pypdf==6.1.3](https://github.com/py-pdf/pypdf/releases/tag/6.1.3).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3502](https://github.com/py-pdf/pypdf/pull/3502).
