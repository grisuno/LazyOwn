# Dependabot Alert #29: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-41168
- **Created:** 2026-06-07T17:50:24Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/29

## Summary
pypdf has long runtimes for wrong size values in cross-reference and object streams

## Description
### Impact

An attacker who uses this vulnerability can craft a PDF which leads to long runtimes. This requires cross-reference streams with wrong large `/Size` values or object streams with wrong large `/N` values.

### Patches

This has been fixed in [pypdf==6.10.1](https://github.com/py-pdf/pypdf/releases/tag/6.10.1).

### Workarounds

If you cannot upgrade yet, consider applying the changes from PR [#3733](https://github.com/py-pdf/pypdf/pull/3733).
