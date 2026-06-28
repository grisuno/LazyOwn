# Dependabot Alert #36: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-48155
- **Created:** 2026-06-12T19:00:20Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/36

## Summary
pypdf: Possible large memory usage for large offsets for layout mode text

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to large memory usage. This requires extracting text in layout mode with large character offsets.

### Patches

This has been fixed in [pypdf==6.12.0](https://github.com/py-pdf/pypdf/releases/tag/6.12.0).

### Workarounds

If developers are unable to immediately upgrade, they should consider applying the changes from PR [#3790](https://github.com/py-pdf/pypdf/pull/3790).
