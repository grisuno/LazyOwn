# Dependabot Alert #30: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-41312
- **Created:** 2026-06-07T17:50:24Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/30

## Summary
pypdf: Manipulated FlateDecode predictor parameters can exhaust RAM

## Description
### Impact
An attacker who uses this vulnerability can craft a PDF which leads to the RAM being exhausted. This requires accessing a stream compressed using `/FlateDecode` with a `/Predictor` unequal 1 and large predictor parameters.

### Patches
This has been fixed in [pypdf==6.10.2](https://github.com/py-pdf/pypdf/releases/tag/6.10.2).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3734](https://github.com/py-pdf/pypdf/pull/3734).
