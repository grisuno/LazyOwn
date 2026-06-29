# Dependabot Alert #43: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-48735
- **Created:** 2026-06-20T09:41:17Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/43

## Summary
pypdf: Manipulated XMP metadata streams can exhaust RAM

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to large memory usage. This requires parsing large XMP metadata, possibly with lots of unnecessary elements.

### Patches
This has been fixed in [pypdf==6.12.1](https://github.com/py-pdf/pypdf/releases/tag/6.12.1).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3796](https://github.com/py-pdf/pypdf/pull/3796).
