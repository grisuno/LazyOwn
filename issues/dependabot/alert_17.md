# Dependabot Alert #17: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-27024
- **Created:** 2026-06-07T17:50:22Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/17

## Summary
pypdf has a possible infinite loop when processing TreeObject

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to an infinite loop. This requires accessing the children of a `TreeObject`, for example as part of outlines.

### Patches

This has been fixed in [pypdf==6.7.1](https://github.com/py-pdf/pypdf/releases/tag/6.7.1).

### Workarounds

If you cannot upgrade yet, consider applying the changes from PR [#3645](https://github.com/py-pdf/pypdf/pull/3645).
