# Dependabot Alert #22: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-28351
- **Created:** 2026-06-07T17:50:23Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/22

## Summary
pypdf: Manipulated RunLengthDecode streams can exhaust RAM

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to large memory usage. This requires parsing the content stream using the RunLengthDecode filter.

### Patches
This has been fixed in [pypdf==6.7.4](https://github.com/py-pdf/pypdf/releases/tag/6.7.4).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3664](https://github.com/py-pdf/pypdf/pull/3664).
