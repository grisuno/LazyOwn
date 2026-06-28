# Dependabot Alert #31: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-41313
- **Created:** 2026-06-07T17:50:24Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/31

## Summary
pypdf: Possible long runtimes for wrong size values in incremental mode

## Description
### Impact
An attacker who uses this vulnerability can craft a PDF which leads to long runtimes. This requires loading a PDF with a large trailer `/Size` value in incremental mode.

### Patches
This has been fixed in [pypdf==6.10.2](https://github.com/py-pdf/pypdf/releases/tag/6.10.2).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3735](https://github.com/py-pdf/pypdf/pull/3735).
