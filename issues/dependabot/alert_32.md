# Dependabot Alert #32: pypdf

- **State:** open
- **Severity:** medium
- **CVE:** CVE-2026-41314
- **Created:** 2026-06-07T17:50:24Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/32

## Summary
pypdf: Manipulated FlateDecode image dimensions can exhaust RAM

## Description
### Impact
An attacker who uses this vulnerability can craft a PDF which leads to the RAM being exhausted. This requires accessing an image using `/FlateDecode` with large size values.

### Patches
This has been fixed in [pypdf==6.10.2](https://github.com/py-pdf/pypdf/releases/tag/6.10.2).

### Workarounds
If you cannot upgrade yet, consider applying the changes from PR [#3734](https://github.com/py-pdf/pypdf/pull/3734).
