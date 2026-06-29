# Dependabot Alert #35: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-48156
- **Created:** 2026-06-12T19:00:07Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/35

## Summary
pypdf: Possible long runtimes for zero-only width values in cross-reference streamsuntimes for zero-only width values in cross-reference streams

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to long runtimes. This requires cross-reference streams with `/W [0 0 0]` values and large `/Size` values.

### Patches

This has been fixed in [pypdf==6.12.0](https://github.com/py-pdf/pypdf/releases/tag/6.12.0).

### Workarounds

If developers are unable to upgrade their apps immediately, they should consider applying the changes from PR [#3791](https://github.com/py-pdf/pypdf/pull/3791).
