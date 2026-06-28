# Dependabot Alert #25: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-33123
- **Created:** 2026-06-07T17:50:23Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/25

## Summary
pypdf has inefficient decoding of array-based streams

## Description
### Impact
An attacker who uses this vulnerability can craft a PDF which leads to long runtimes and/or large memory usage. This requires accessing an array-based stream with lots of entries.

### Patches
This has been fixed in [pypdf==6.9.1](https://github.com/py-pdf/pypdf/releases/tag/6.9.1).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3686](https://github.com/py-pdf/pypdf/pull/3686).
